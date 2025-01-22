import os
import subprocess
from collections import defaultdict, deque
import clang.cindex

# Output directories
OUTPUT_DIR = "output"
SEGMENT_DIR = os.path.join(OUTPUT_DIR, "segments")

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SEGMENT_DIR, exist_ok=True)


class Symbol:
    """Represents a symbol in the source file."""
    def __init__(self, name, kind, start_line, end_line=None, dependencies=None):
        self.name = name
        self.kind = kind
        self.start_line = start_line
        self.end_line = end_line
        self.dependencies = dependencies or []

    def to_dict(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "dependencies": self.dependencies,
        }

def preprocess_with_cpp(file, include_paths=None, output_dir="output"):
    """
    Preprocess the C file to resolve includes and macros, filtering out system-level code.
    Args:
        file (str): Path to the input C file.
        include_paths (list, optional): List of include paths for headers.
        output_dir (str): Directory to save the preprocessed file.
    Returns:
        str: Path to the preprocessed file.
    """
    preprocessed_file = os.path.join(output_dir, f"preprocessed_{os.path.basename(file)}")
    cmd = ["gcc", "-E", file, "-o", preprocessed_file, "-std=c99"]

    if include_paths:
        for path in include_paths:
            cmd.extend(["-I", path])  # Add include paths

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"Preprocessed file saved at {preprocessed_file}")

        # Filter out system-level includes and incomplete lines
        with open(preprocessed_file, "r") as f:
            lines = f.readlines()

        filtered_lines = [
            line for line in lines
            if not line.startswith("#") and
            not line.strip().startswith("typedef struct") and
            not line.strip().startswith("{")
        ]

        with open(preprocessed_file, "w") as f:
            f.writelines(filtered_lines)

        print(f"Filtered preprocessed file saved at {preprocessed_file}")
        return preprocessed_file

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Preprocessing failed: {e.stderr.decode()}")

def remove_blank_lines(file_path):
    """
    Remove blank lines from a file.
    Args:
        file_path (str): Path to the file.
    Returns:
        str: Path to the cleaned file.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    non_empty_lines = [line for line in lines if line.strip()]
    with open(file_path, "w") as f:
        f.writelines(non_empty_lines)
    print(f"Blank lines removed from {file_path}")
    return file_path


def process_macros(file):
    """
    Process macros and generate a simplified source file.
    Args:
        file (str): Path to the preprocessed file.
    Returns:
        str: Path to the processed file with macros simplified.
    """
    macros = []
    processed_lines = []

    with open(file, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#define"):
                macros.append(stripped)
            elif stripped.startswith("#ifdef") or stripped.startswith("#ifndef"):
                condition = stripped.split()[1]
                processed_lines.append(f"// Macro condition: {condition}\n")
            elif stripped.startswith("#endif"):
                continue
            else:
                processed_lines.append(line)

    macros_file = os.path.join(OUTPUT_DIR, "macros.txt")
    with open(macros_file, "w") as mf:
        mf.write("\n".join(macros))
    print(f"Macros saved at {macros_file}")

    processed_file = os.path.join(OUTPUT_DIR, "processed_macros.c")
    with open(processed_file, "w") as pf:
        pf.writelines(processed_lines)
    print(f"Processed file saved at {processed_file}")
    return processed_file

def extract_contextual_info(file):
    """
    Extract user-defined symbols and ensure no overlapping ranges.
    Args:
        file (str): Path to the processed file.
    Returns:
        list: A list of Symbol objects.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    symbols = []
    seen_ranges = set()

    def traverse_ast(cursor):
        if cursor.location.file and os.path.samefile(cursor.location.file.name, file):
            if cursor.kind in (
                clang.cindex.CursorKind.FUNCTION_DECL,
                clang.cindex.CursorKind.VAR_DECL,
            ):
                start_line = cursor.location.line
                end_line = cursor.extent.end.line

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
    print(f"Extracted {len(symbols)} user-defined symbols.")
    return symbols

def build_dependency_graph(symbols):
    """
    Build a dependency graph from symbols, ignoring external dependencies.
    """
    graph = defaultdict(list)
    nodes = {symbol.name for symbol in symbols}

    for symbol in symbols:
        for dependency in symbol.dependencies:
            if dependency in nodes:
                graph[symbol.name].append(dependency)
            else:
                # Ignore unresolved external dependencies
                print(f"Ignoring unresolved external dependency: {dependency}")

    # Ensure all nodes are included, even if they have no dependencies
    for symbol in symbols:
        if symbol.name not in graph:
            graph[symbol.name] = []

    return graph


def topological_sort(graph):
    """Perform a topological sort on the dependency graph."""
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

def dynamic_segment_code(file, symbols, max_complexity):
    """
    Segment the code dynamically, creating a separate segment for each symbol.
    Args:
        file (str): Path to the processed file.
        symbols (list): List of Symbol objects.
        max_complexity (int): Maximum complexity per segment.
    Returns:
        list: A list of segment file paths.
    """
    segments = []

    with open(file, "r") as f:
        lines = f.readlines()

    # Process each symbol individually
    for idx, symbol in enumerate(symbols):
        start, end = symbol.start_line - 1, symbol.end_line

        # Skip invalid ranges
        if start < 0 or end > len(lines):
            continue

        # Extract lines for this symbol
        segment_lines = lines[start:end]

        # Save the segment
        segment_file = os.path.join(SEGMENT_DIR, f"segment_{idx}.c")
        with open(segment_file, "w") as f:
            f.writelines(segment_lines)
        print(f"Segment saved: {segment_file}")
        segments.append(segment_file)

    print(f"Total segments created: {len(segments)}")
    return segments


def save_segment(segments, segment_lines):
    """Save a segment to the output directory."""
    segment_file = os.path.join(SEGMENT_DIR, f"segment_{len(segments)}.c")
    with open(segment_file, "w") as f:
        f.writelines(segment_lines)
    print(f"Segment saved: {segment_file}")
    return segment_file
