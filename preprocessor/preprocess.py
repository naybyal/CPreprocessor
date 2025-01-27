import os
import re
import subprocess
import json
from collections import defaultdict, deque
import clang.cindex

# Constants for output directories
OUTPUT_DIR = "output"
SEGMENT_DIR = os.path.join(OUTPUT_DIR, "segments")

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SEGMENT_DIR, exist_ok=True)


class Symbol:
    """Represents a symbol in the source file."""
    def __init__(self, name, kind, start_line, end_line=None, dependencies=None, segment=None):
        self.name = name
        self.kind = kind
        self.start_line = start_line
        self.end_line = end_line
        self.dependencies = dependencies or []
        self.segment = segment

    def to_dict(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "dependencies": self.dependencies,
        }


def preprocess_with_cpp(input_file, include_paths=None, output_dir=OUTPUT_DIR):
    """
    Preprocess a C file using the GCC preprocessor.
    """
    include_paths = include_paths or []
    standard_include_paths = ["/usr/include", "/usr/lib/gcc/x86_64-linux-gnu/12/include"]
    include_paths.extend(standard_include_paths)

    include_flags = [f"-I{path}" for path in include_paths]
    preprocessed_file = os.path.join(output_dir, f"preprocessed_{os.path.basename(input_file)}")
    cmd = ["gcc", "-E", *include_flags, input_file, "-o", preprocessed_file, "-std=c99"]

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Preprocessing failed: {e.stderr.decode()}")

    return preprocessed_file


def extract_user_defined_includes(file):
    """
    Extract user-defined include paths from the input file (headers in double quotes).
    """
    include_pattern = re.compile(r'#include\s+"(.+?)"')
    user_defined_paths = set()

    with open(file, "r") as f:
        for line in f:
            match = include_pattern.search(line)
            if match:
                include_file = match.group(1)
                user_defined_paths.add(os.path.dirname(include_file))

    return list(user_defined_paths)


def remove_blank_lines(file_path):
    """
    Remove blank lines from a file.
    """
    with open(file_path, "r") as f:
        lines = [line for line in f if line.strip()]

    with open(file_path, "w") as f:
        f.writelines(lines)

    return file_path


def process_macros(file):
    """
    Separate macros (#define) from the source file and save them separately.
    """
    macros, processed_lines = [], []

    with open(file, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#define"):
                macros.append(stripped)
            else:
                processed_lines.append(line)

    macros_file = os.path.join(OUTPUT_DIR, "macros.txt")
    processed_file = os.path.join(OUTPUT_DIR, "processed_macros.c")

    with open(macros_file, "w") as mf:
        mf.write("\n".join(macros))

    with open(processed_file, "w") as pf:
        pf.writelines(processed_lines)

    return processed_file


def extract_contextual_info(file):
    """
    Extract symbols (functions, structs, variables, etc.) and their dependencies using Clang.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    symbols = []
    seen_ranges = set()

    def traverse_ast(cursor):
        # Process only nodes within the input file
        if cursor.location.file and os.path.samefile(cursor.location.file.name, file):
            if cursor.kind in (
                clang.cindex.CursorKind.FUNCTION_DECL,
                clang.cindex.CursorKind.VAR_DECL,
                clang.cindex.CursorKind.STRUCT_DECL,
                clang.cindex.CursorKind.UNION_DECL,
                clang.cindex.CursorKind.CLASS_DECL,
                clang.cindex.CursorKind.ENUM_DECL,
                clang.cindex.CursorKind.TYPEDEF_DECL,
            ):
                start_line, end_line = cursor.location.line, cursor.extent.end.line

                # Skip overlapping ranges
                if (start_line, end_line) in seen_ranges:
                    return

                symbols.append(
                    Symbol(
                        name=cursor.spelling,
                        kind=str(cursor.kind),
                        start_line=start_line,
                        end_line=end_line,
                        dependencies=[
                            ref.spelling for ref in cursor.get_children() if ref.kind.is_reference()
                        ],
                    )
                )
                seen_ranges.add((start_line, end_line))

        for child in cursor.get_children():
            traverse_ast(child)

    traverse_ast(translation_unit.cursor)
    return symbols


def build_dependency_graph(symbols):
    """
    Build a dependency graph from extracted symbols.
    """
    graph = defaultdict(list)
    nodes = {symbol.name for symbol in symbols}

    for symbol in symbols:
        for dependency in symbol.dependencies:
            if dependency in nodes:
                graph[symbol.name].append(dependency)

    return graph


def topological_sort(graph):
    """
    Perform a topological sort on the dependency graph.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for dependency in graph[node]:
            in_degree[dependency] += 1

    queue = deque([node for node in graph if in_degree[node] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(graph):
        raise ValueError("Dependency graph has cycles!")

    return sorted_order


def dynamic_segment_code(file, symbols):
    """
    Segment code based on extracted symbols and save each segment to a file.
    """
    with open(file, "r") as f:
        lines = f.readlines()

    segments = []
    for idx, symbol in enumerate(symbols):
        start, end = symbol.start_line - 1, symbol.end_line
        if start < 0 or end > len(lines):
            continue

        segment_file = os.path.join(SEGMENT_DIR, f"segment_{idx}.c")
        with open(segment_file, "w") as seg_file:
            seg_file.writelines(lines[start:end])
        segments.append(segment_file)

    return segments


def is_unnecessary_segment(segment_content):
    """
    Determine if a segment is unnecessary based on its content.
    """
    return bool(
        re.match(r"^extern\s+\w+\s*\*?\w+;$", segment_content) or  # Extern declarations
        not segment_content.strip()  # Empty or whitespace-only
    )


def filter_segments(symbols, segments):
    """
    Filter meaningful segments and generate metadata for the final output.
    """
    meaningful_segments, metadata = [], []
    symbol_ranges = {(symbol.start_line, symbol.end_line): symbol.to_dict() for symbol in symbols}

    for idx, segment_file in enumerate(segments):
        with open(segment_file, "r") as f:
            content = f.read()

        associated_symbols = [
            symbol for (start, end), symbol in symbol_ranges.items() if start - 1 <= idx < end
        ]

        if associated_symbols and not is_unnecessary_segment(content):
            meaningful_segments.append(segment_file)
            metadata.append({"segment": segment_file, "symbols": associated_symbols})
        else:
            os.remove(segment_file)

    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    return meaningful_segments
