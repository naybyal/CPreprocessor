import os
import re
import uuid
import subprocess

def extract_user_defined_includes(file):
    """Extracts user-defined includes, ignoring system headers."""
    include_pattern = re.compile(r'^\s*#include\s*"(.+?)"', re.MULTILINE)
    includes = []
    base_dir = os.path.dirname(os.path.abspath(file))

    with open(file, "r") as f:
        content = f.read()
        for match in include_pattern.finditer(content):
            include_path = os.path.join(base_dir, match.group(1))
            if os.path.exists(include_path):
                includes.append(include_path)
    return includes

def merge_user_includes(file):
    """Recursively merges user-defined includes into the main file while avoiding all #include directives."""
    processed = set()

    def merge(file_path):
        if file_path in processed:
            return ""  # Avoid circular includes
        processed.add(file_path)

        with open(file_path, "r") as f:
            content = f.readlines()

        merged_content = []
        user_include_pattern = re.compile(r'^\s*#include\s*"(.+?)"')
        system_include_pattern = re.compile(r'^\s*#include\s*<.+?>')

        for line in content:
            # Handle user includes
            user_match = user_include_pattern.match(line)
            if user_match:
                include_file = user_match.group(1)
                include_path = os.path.join(os.path.dirname(file_path), include_file)
                if os.path.exists(include_path):
                    merged_content.append(merge(include_path))
                continue
            
            # Skip system includes
            if system_include_pattern.match(line):
                continue
            
            # Add all other lines
            merged_content.append(line)

        return "".join(merged_content)

    return merge(file)

def preprocess_c_file(input_file, output_dir="output"):
    """Preprocesses the C file by merging user-defined includes, expanding macros, and removing all includes."""
    os.makedirs(output_dir, exist_ok=True)
    merged_file_path = os.path.join(output_dir, f"merged_{os.path.basename(input_file)}")

    # Merge user-defined includes and remove all #include directives
    merged_content = merge_user_includes(input_file)
    with open(merged_file_path, "w") as f:
        f.write(merged_content)

    # Expand macros using GCC preprocessor while ignoring system includes
    preprocessed_file = os.path.join(output_dir, "preprocessed.c")
    cmd = [
        "gcc", 
        "-nostdinc",       # Prevent standard system includes
        "-ffreestanding",  # Disable standard library assumptions
        "-E",              # Run preprocessor
        "-dD",             # Output macro definitions
        merged_file_path, 
        "-o", preprocessed_file,
        "-std=c99"
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Preprocessing failed:\nCommand: {e.cmd}\nError: {e.stderr.decode()}")

    return preprocessed_file