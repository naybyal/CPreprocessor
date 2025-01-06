import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
from pycparser import parse_file, c_ast, c_generator

# Output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Helper Functions ---
def run_ctags(file: str) -> List[Dict]:
    """
    Use ctags to extract functions, types, and macros from the C file.
    """
    command = f"ctags -x --c-kinds=+fpst {file}"  # Extract functions, prototypes, structs, typedefs
    result = os.popen(command).read()
    if not result.strip():
        print(f"No symbols found in {file}. Ensure ctags is installed and file has valid content.")
        return []

    parsed_data = []
    for line in result.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 4:
            symbol, kind, line_num = parts[0], parts[1], int(parts[2])
            parsed_data.append({"symbol": symbol, "kind": kind, "line": line_num})
    return parsed_data


def parse_with_pycparser(file: str) -> c_ast.FileAST:
    """
    Parse the C file using pycparser to generate an abstract syntax tree (AST).
    """
    try:
        ast = parse_file(file, use_cpp=True, cpp_path="gcc", cpp_args=["-E", "-std=c99"])
        return ast
    except Exception as e:
        print(f"Error parsing {file} with pycparser: {e}")
        return None


# --- Preprocessor Steps ---
def merge_modules(c_files: List[str]) -> str:
    """
    Merge all C files into a single module by inlining #include directives.
    """
    merged_content = []
    for file in c_files:
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.strip().startswith("#include"):
                # Inline the header file's content
                included_file = line.strip().split('"')[1] if '"' in line else None
                if included_file and os.path.exists(included_file):
                    with open(included_file, "r") as header:
                        merged_content.append(f"// Start of {included_file}\n")
                        merged_content.extend(header.readlines())
                        merged_content.append(f"// End of {included_file}\n")
                else:
                    merged_content.append(line)
            else:
                merged_content.append(line)

    # Save the merged module
    merged_file = os.path.join(OUTPUT_DIR, "merged.c")
    with open(merged_file, "w") as f:
        f.writelines(merged_content)

    print(f"Merged module saved as {merged_file}")
    return merged_file


def reorder_code(file: str, parsed_data: List[Dict]) -> str:
    """
    Reorder the C code based on dependencies and function definitions.
    """
    with open(file, "r") as f:
        lines = f.readlines()

    reordered_content = []
    seen_lines = set()

    # Reorder based on parsed symbols (functions, types, etc.)
    for symbol in parsed_data:
        line_num = symbol["line"] - 1
        if 0 <= line_num < len(lines) and line_num not in seen_lines:
            reordered_content.append(lines[line_num])
            seen_lines.add(line_num)

    # Append remaining lines (not part of parsed symbols)
    for i, line in enumerate(lines):
        if i not in seen_lines:
            reordered_content.append(line)

    # Save the reordered file
    reordered_file = os.path.join(OUTPUT_DIR, "reordered.c")
    with open(reordered_file, "w") as f:
        f.writelines(reordered_content)

    print(f"Reordered file saved as {reordered_file}")
    return reordered_file


def handle_macros(file: str) -> str:
    """
    Handle C macros and convert them for Rust compatibility.
    """
    with open(file, "r") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if line.startswith("#define"):
            # Convert macros to comments
            updated_lines.append(f"// Converted macro: {line.strip()}\n")
        elif line.startswith("#ifdef"):
            # Handle conditional compilation
            updated_lines.append(f"// Converted conditional compilation: {line.strip()}\n")
        else:
            updated_lines.append(line)

    # Save the macro-handled file
    macro_file = os.path.join(OUTPUT_DIR, "macros_handled.c")
    with open(macro_file, "w") as f:
        f.writelines(updated_lines)

    print(f"Macro-handled file saved as {macro_file}")
    return macro_file


def segment_code(file: str, segment_size: int = 50) -> List[str]:
    """
    Segment the code into smaller translation units for the LLM.
    """
    with open(file, "r") as f:
        lines = f.readlines()

    segments = []
    current_segment = []
    segment_count = 0

    for i, line in enumerate(lines):
        current_segment.append(line)
        if (i + 1) % segment_size == 0 or i == len(lines) - 1:
            segment_file = os.path.join(OUTPUT_DIR, f"segment_{segment_count}.c")
            with open(segment_file, "w") as seg_file:
                seg_file.writelines(current_segment)
            segments.append(segment_file)
            current_segment = []
            segment_count += 1

    print(f"Segmented file into {len(segments)} parts.")
    return segments


def generate_metadata(parsed_data: List[Dict], segments: List[str]) -> str:
    """
    Generate JSON metadata for context supplementation.
    """
    metadata = {
        "symbols": parsed_data,
        "segments": [{"file": seg, "lines": len(open(seg).readlines())} for seg in segments],
    }

    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Metadata saved as {metadata_file}")
    return metadata_file


def preprocess(c_files: List[str], segment_size: int = 50):
    """
    Full preprocessing pipeline:
    - Merge modules
    - Parse symbols (ctags)
    - Reorder code
    - Handle macros
    - Segment code
    - Generate metadata
    """
    print("Merging modules...")
    merged_file = merge_modules(c_files)

    print("Running ctags for static analysis...")
    ctags_data = run_ctags(merged_file)

    print("Reordering code...")
    reordered_file = reorder_code(merged_file, ctags_data)

    print("Handling macros...")
    macro_file = handle_macros(reordered_file)

    print("Segmenting code...")
    segments = segment_code(macro_file, segment_size)

    print("Generating metadata...")
    metadata_file = generate_metadata(ctags_data, segments)

    print(f"Preprocessing complete. Outputs saved in {OUTPUT_DIR}")


if __name__ == "__main__":
    input_files = ["main.c", "stdio.h"]  # Replace with your actual C files
    preprocess(input_files, segment_size=50)
