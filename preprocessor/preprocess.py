import os
import re
import subprocess
import uuid

def extract_user_defined_includes(file):
    """Extract user-defined includes (ignoring system headers)."""
    include_pattern = re.compile(r'#include\s+"(.+?)"')
    includes = []
    base_dir = os.path.dirname(os.path.abspath(file))

    with open(file, "r") as f:
        for line in f:
            match = include_pattern.search(line)
            if match:
                include_path = os.path.join(base_dir, match.group(1))
                if os.path.exists(include_path):
                    includes.append(include_path)
    return includes

def merge_user_includes(file):
    """Recursively merge user-defined includes into the main file."""
    processed = set()

    def merge(file_path):
        if file_path in processed:
            return ""  # Avoid circular includes
        processed.add(file_path)

        with open(file_path, "r") as f:
            content = f.readlines()

        merged_content = []
        for line in content:
            match = re.match(r'#include\s+"(.+?)"', line)
            if match:
                include_path = os.path.join(os.path.dirname(file_path), match.group(1))
                if os.path.exists(include_path):
                    merged_content.append(merge(include_path))  # Recursively merge
            else:
                merged_content.append(line)

        return "".join(merged_content)

    return merge(file)

def preprocess_c_file(input_file, output_dir="output"):
    """Preprocess the C file by merging user-defined includes and removing system includes."""
    os.makedirs(output_dir, exist_ok=True)
    merged_file_path = os.path.join(output_dir, f"merged_{uuid.uuid4().hex}_{os.path.basename(input_file)}")

    merged_content = merge_user_includes(input_file)
    with open(merged_file_path, "w") as f:
        f.write(merged_content)

    return merged_file_path
