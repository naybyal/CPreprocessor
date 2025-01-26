import os
import re
import subprocess
import json
from collections import defaultdict, deque
import uuid
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


def parse_header_files(headers, include_paths):
    """
    Recursively parse header files and extract symbols.
    """
    symbols = []
    visited = set()
    index = clang.cindex.Index.create()

    def parse_file(file_path):
        if file_path in visited:
            return
        visited.add(file_path)

        try:
            tu = index.parse(file_path, args=[f"-I{path}" for path in include_paths])
            symbols.extend(extract_symbols_from_ast(tu.cursor, file_path))
        except Exception as e:
            print(f"Error parsing header {file_path}: {e}")

    for header in headers:
        parse_file(header)

    return symbols


def extract_symbols_from_ast(cursor, file):
    """
    Extract symbols from the AST of a given file.
    """
    symbols = []
    seen_ranges = set()

    def traverse_ast(node):
        if node.location.file and os.path.samefile(node.location.file.name, file):
            if node.kind in (
                clang.cindex.CursorKind.FUNCTION_DECL,
                clang.cindex.CursorKind.VAR_DECL,
                clang.cindex.CursorKind.STRUCT_DECL,
                clang.cindex.CursorKind.UNION_DECL,
                clang.cindex.CursorKind.CLASS_DECL,
                clang.cindex.CursorKind.ENUM_DECL,
                clang.cindex.CursorKind.TYPEDEF_DECL,
            ) and node.is_definition():
                start_line, end_line = node.location.line, node.extent.end.line
                if (start_line, end_line) not in seen_ranges:
                    symbols.append(
                        Symbol(
                            name=node.spelling,
                            kind=str(node.kind),
                            start_line=start_line,
                            end_line=end_line,
                            dependencies=[ref.spelling for ref in node.get_children() if ref.kind.is_reference()],
                        )
                    )
                    seen_ranges.add((start_line, end_line))

        for child in node.get_children():
            traverse_ast(child)

    traverse_ast(cursor)
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


def segment_code(file, symbols):
    """
    Segment code based on extracted symbols and save each segment to a file.
    """
    with open(file, "r") as f:
        lines = f.readlines()

    segments = []
    for symbol in symbols:
        start, end = symbol.start_line - 1, symbol.end_line
        if start < 0 or end > len(lines):
            continue

        segment_file = os.path.join(SEGMENT_DIR, f"{symbol.name}_{uuid.uuid4().hex}.c")
        with open(segment_file, "w") as seg_file:
            seg_file.writelines(lines[start:end])
        segments.append((segment_file, symbol))

    return segments


def filter_meaningful_segments(segments):
    """
    Filter meaningful segments based on refined criteria.
    """
    meaningful_segments = []
    metadata = []

    for segment_file, symbol in segments:
        with open(segment_file, "r") as f:
            content = f.read()

        if not content.strip():
            os.remove(segment_file)
            continue

        meaningful_segments.append(segment_file)
        metadata.append({
            "segment": segment_file,
            "symbol": symbol.to_dict(),
        })

    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    return meaningful_segments


def main(input_file):
    user_defined_includes = extract_user_defined_includes(input_file)
    preprocessed_file = preprocess_with_cpp(input_file, user_defined_includes)
    header_symbols = parse_header_files(user_defined_includes, user_defined_includes)
    file_symbols = extract_symbols_from_ast(clang.cindex.Index.create().parse(preprocessed_file).cursor, preprocessed_file)
    symbols = file_symbols + header_symbols

    dependency_graph = build_dependency_graph(symbols)
    sorted_symbols = [symbol for name in topological_sort(dependency_graph) for symbol in symbols if symbol.name == name]
    segments = segment_code(preprocessed_file, sorted_symbols)
    meaningful_segments = filter_meaningful_segments(segments)

    print("Meaningful segments saved:", meaningful_segments)


if __name__ == "__main__":
    clang.cindex.Config.set_library_file("/usr/lib/x86_64-linux-gnu/libclang-14.so")  # Adjust for your environment
    main("main.c")
