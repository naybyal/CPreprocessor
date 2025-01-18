import os
import subprocess
import json
from collections import defaultdict

import clang.cindex

OUTPUT_DIR = "output"
SEGMENT_DIR = "segments"

# Symbol metadata structure
class Symbol:
    def __init__(self, symbol, kind, start_line, end_line=None):
        self.symbol = symbol
        self.kind = kind
        self.start_line = start_line
        self.end_line = end_line

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'kind': self.kind,
            'start_line': self.start_line,
            'end_line': self.end_line,
        }

# Segment metadata structure
class Segment:
    def __init__(self, file, lines):
        self.file = file
        self.lines = lines

    def to_dict(self):
        return {
            'file': self.file,
            'lines': self.lines,
        }

# Full metadata structure
class Metadata:
    def __init__(self, symbols, segments):
        self.symbols = symbols
        self.segments = segments

    def to_dict(self):
        return {
            'symbols': [s.to_dict() for s in self.symbols],
            'segments': [s.to_dict() for s in self.segments],
        }

def create_output_dir():
    """Create the output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_with_cpp(file):
    """Preprocess a single C file using the C preprocessor."""
    output_file = os.path.join(OUTPUT_DIR, f"preprocessed_{os.path.basename(file)}")
    cleaned_file = os.path.join(OUTPUT_DIR, f"cleaned_{os.path.basename(file)}")
    
    try:
        # Run the preprocessor
        subprocess.run(
            ["gcc", "-E", file, "-o", output_file, "-std=c99"],
            capture_output=True,
            text=True,
            check=True  # Raise an exception if the command fails
        )
        print(f"Preprocessed file saved as {output_file}")
        
        # Remove unnecessary empty lines
        with open(output_file, "r") as f:
            lines = [line for line in f if line.strip()]  # Only keep non-empty lines
        
        with open(cleaned_file, "w") as f:
            f.writelines(lines)
        
        print(f"Cleaned file with unnecessary empty lines removed saved as {cleaned_file}")
        return cleaned_file

    except subprocess.CalledProcessError as e:
        raise Exception(f"C preprocessor failed for {file}: {e.stderr}") from e


def extract_contextual_info(file):
    """Extract contextual information using Clang."""
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    symbols = []

    def traverse_ast(cursor):
        """Recursively traverse the AST."""
        try:
            if cursor.kind in (
                clang.cindex.CursorKind.FUNCTION_DECL,
                clang.cindex.CursorKind.VAR_DECL,
                clang.cindex.CursorKind.STRUCT_DECL,
                clang.cindex.CursorKind.UNION_DECL,
                clang.cindex.CursorKind.TYPEDEF_DECL,
                clang.cindex.CursorKind.ENUM_DECL,
                clang.cindex.CursorKind.ENUM_CONSTANT_DECL,
                clang.cindex.CursorKind.FIELD_DECL,
                clang.cindex.CursorKind.PARM_DECL,
                clang.cindex.CursorKind.TYPE_REF,
                clang.cindex.CursorKind.CXX_METHOD,  # For C++ methods (if needed)
                clang.cindex.CursorKind.NAMESPACE,  # For C++ namespaces (if needed)
                clang.cindex.CursorKind.CONSTRUCTOR,  # For C++ constructors (if needed)
                clang.cindex.CursorKind.DESTRUCTOR,  # For C++ destructors (if needed)
                # ... add other relevant CursorKinds as needed ...
            ):
                symbols.append(
                    Symbol(
                        cursor.spelling,
                        str(cursor.kind),
                        cursor.location.line,
                        cursor.extent.end.line,
                    )
                )
        except ValueError as e:
            print(f"Error processing symbol: {cursor.spelling} - {e}")

        for child in cursor.get_children():
            traverse_ast(child)

    traverse_ast(translation_unit.cursor)
    return symbols

def handle_macros_with_clang(file):
    """Handle macros with Clang preprocessing."""
    output_file = os.path.join(OUTPUT_DIR, "macros_handled.c")
    try:
        subprocess.run(
            ["clang", "-E", file, "-o", output_file, "-std=c99"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Clang preprocessing failed: {e.stderr}") from e
    print(f"Macro-handled file saved as {output_file}")
    return output_file


def segment_code(file, symbols, max_lines):
    os.makedirs(SEGMENT_DIR, exist_ok=True)
    
    with open(file, "r") as f:
        lines = f.readlines()

    segments = []
    current_segment = []
    current_line_count = 0
    last_end = 0

    for symbol in symbols:
        start, end = symbol.start_line - 1, symbol.end_line
        # Add lines before the symbol starts
        if start > last_end:
            current_segment.extend(lines[last_end:start])
            current_line_count += start - last_end

        # Create new segment if current exceeds max_lines
        if current_line_count + (end - start) > max_lines:
            segment_file = os.path.join(SEGMENT_DIR, f"segment_{len(segments)}.c")
            with open(segment_file, "w") as sf:
                sf.writelines(current_segment)
            segments.append(Segment(segment_file, len(current_segment)))
            current_segment = []
            current_line_count = 0

        current_segment.extend(lines[start:end])
        current_line_count += end - start
        last_end = end

    # Handle remaining lines
    if current_segment:
        segment_file = os.path.join(SEGMENT_DIR, f"segment_{len(segments)}.c")
        with open(segment_file, "w") as sf:
            sf.writelines(current_segment)
        segments.append(Segment(segment_file, len(current_segment)))

    print(f"Segmented into {len(segments)} parts.")
    return segments


def generate_metadata(symbols, segments):
    """Generate JSON metadata."""
    metadata = Metadata(symbols, segments)
    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata.to_dict(), f, indent=4)
    print(f"Metadata saved as {metadata_file}")
    return metadata_file

def preprocess(c_file, max_lines):
    """Full preprocessing pipeline."""
    create_output_dir()

    print("Running the C preprocessor...")
    preprocessed_file = preprocess_with_cpp(c_file)

    print("Extracting contextual information...")
    symbols = extract_contextual_info(preprocessed_file)

    print("Reordering code...")
    reordered_file = handle_macros_with_clang(preprocessed_file)

    print("Segmenting code...")
    segments = segment_code(reordered_file, symbols, max_lines)

    print("Generating metadata...")
    generate_metadata(symbols, segments)

    print(f"Preprocessing complete. Outputs saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    input_file = "main.c"
    clang.cindex.Config.set_library_file("/usr/lib/x86_64-linux-gnu/libclang-14.so.14.0.6")
    preprocess(input_file, max_lines=100)