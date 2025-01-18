import os
import subprocess
import json
from collections import defaultdict, deque
import clang.cindex

# Output directories
OUTPUT_DIR = "output"
SEGMENT_DIR = "segments"

# Symbol structure
class Symbol:
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


# Segment structure
class Segment:
    def __init__(self, file, lines):
        self.file = file
        self.lines = lines

    def to_dict(self):
        return {"file": self.file, "lines": self.lines}


def create_output_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(SEGMENT_DIR, exist_ok=True)


def preprocess_with_cpp(file):
    """Preprocess the C file using GCC."""
    output_file = os.path.join(OUTPUT_DIR, f"preprocessed_{os.path.basename(file)}")
    try:
        subprocess.run(
            ["gcc", "-E", file, "-o", output_file, "-std=c99", "-DSSP_H", "-I/usr/include", "-I/usr/include/linux"],
            check=True,
            stderr=subprocess.PIPE,
        )
        print(f"Preprocessed file saved at {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Preprocessing failed: {e.stderr.decode()}")


def remove_blank_lines(file_path):
    """Remove all blank lines from the specified file."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Filter out blank or whitespace-only lines
    non_empty_lines = [line for line in lines if line.strip()]

    with open(file_path, "w") as f:
        f.writelines(non_empty_lines)

    print(f"Blank lines removed from {file_path}")
    return file_path  # Return the cleaned file path


def process_macros(file):
    """Detect and handle C macros, converting them to Rust-compatible formats."""
    macros = []
    processed_lines = []
    with open(file, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#define"):
                macros.append(stripped)
                continue
            elif stripped.startswith("#ifdef") or stripped.startswith("#ifndef"):
                condition = stripped.split()[1]
                processed_lines.append(f"#[cfg({condition})]\n")
                continue
            elif stripped.startswith("#endif"):
                continue
            processed_lines.append(line)

    macros_file = os.path.join(OUTPUT_DIR, "macros.txt")
    with open(macros_file, "w") as mf:
        mf.write("\n".join(macros))
    print(f"Macros saved at {macros_file}")

    processed_file = os.path.join(OUTPUT_DIR, "processed_macros.c")
    with open(processed_file, "w") as pf:
        pf.writelines(processed_lines)
    print(f"Macros processed and saved at {processed_file}")
    return processed_file, macros_file


def extract_contextual_info(file):
    """Extract symbols and dependencies using Clang."""
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    symbols = []

    def traverse_ast(cursor):
        if cursor.kind in (
            clang.cindex.CursorKind.FUNCTION_DECL,
            clang.cindex.CursorKind.VAR_DECL,
            clang.cindex.CursorKind.STRUCT_DECL,
        ):
            dependencies = [
                ref.spelling for ref in cursor.get_children() if ref.kind.is_reference()
            ]
            symbols.append(
                Symbol(
                    name=cursor.spelling,
                    kind=str(cursor.kind),
                    start_line=cursor.location.line,
                    end_line=cursor.extent.end.line,
                    dependencies=dependencies,
                )
            )
        for child in cursor.get_children():
            traverse_ast(child)

    traverse_ast(translation_unit.cursor)

    for symbol in symbols:
        print(f"Symbol: {symbol.name}, Kind: {symbol.kind}, Start: {symbol.start_line}, End: {symbol.end_line}")
    
    return symbols



def ensure_unique_namespaces(symbols, file):
    """Append unique identifiers to static symbols."""
    file_id = os.path.basename(file).replace(".", "_")
    for symbol in symbols:
        if "static" in symbol.kind.lower():
            symbol.name = f"{symbol.name}_{file_id}"
    print("Ensured unique namespaces for static symbols.")
    return symbols


def build_dependency_graph(symbols):
    """Build a dependency graph from symbols."""
    graph = defaultdict(list)
    nodes = set(symbol.name for symbol in symbols)
    
    for symbol in symbols:
        for dependency in symbol.dependencies:
            if dependency in ["FILE", "size_t"]:  # Ignore common standard library dependencies
                continue

            if dependency in nodes:
                graph[symbol.name].append(dependency)
            else:
                print(f"Ignoring unresolved dependency: {dependency}")

    return graph


def topological_sort(graph):
    """Perform topological sorting on the dependency graph."""
    indegree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1

    queue = deque(node for node in graph if indegree[node] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order


def segment_code(file, symbols, max_complexity):
    """Segment code into smaller parts based on dependency graph and complexity."""
    with open(file, "r") as f:
        lines = f.readlines()

    graph = build_dependency_graph(symbols)
    order = topological_sort(graph)

    if not order:
        print("No dependencies found; processing all symbols sequentially.")
        order = [s.name for s in symbols]

    segments = []
    current_segment = []
    current_complexity = 0
    last_end = 0

    for symbol_name in order:
        symbol = next((s for s in symbols if s.name == symbol_name), None)
        if not symbol:
            print(f"Warning: Symbol {symbol_name} not found.")
            continue

        print(f"Processing symbol: {symbol.name}, Kind: {symbol.kind}, Start: {symbol.start_line}, End: {symbol.end_line}")

        # Skip invalid symbols (e.g., those without a valid range)
        if symbol.start_line is None or symbol.end_line is None or symbol.start_line >= symbol.end_line:
            print(f"Skipping {symbol.name} due to invalid range.")
            continue

        start, end = symbol.start_line - 1, symbol.end_line  # Convert to 0-based index

        # Add lines between symbols to the current segment
        if start > last_end:
            current_segment.extend(lines[last_end:start])
            current_complexity += start - last_end

        # Save the current segment if it exceeds max complexity
        if current_complexity + (end - start) > max_complexity:
            segment_file = os.path.join(SEGMENT_DIR, f"segment_{len(segments)}.c")
            with open(segment_file, "w") as sf:
                sf.writelines(current_segment)
            segments.append(Segment(segment_file, len(current_segment)))
            current_segment = []
            current_complexity = 0

        # Add symbol's lines to the current segment
        current_segment.extend(lines[start:end])
        current_complexity += end - start
        last_end = end

    # Save remaining lines in the last segment if any
    if current_segment:
        segment_file = os.path.join(SEGMENT_DIR, f"segment_{len(segments)}.c")
        with open(segment_file, "w") as sf:
            sf.writelines(current_segment)
        segments.append(Segment(segment_file, len(current_segment)))

    # Fallback: Write the entire file if no segments were created
    if not segments:
        print("No valid segments found; writing entire file as a fallback.")
        segment_file = os.path.join(SEGMENT_DIR, "default_segment.c")
        with open(segment_file, "w") as sf:
            sf.writelines(lines)
        segments.append(Segment(segment_file, len(lines)))
        print(f"Default segment created: {segment_file}")

    print(f"Total segments created: {len(segments)}")
    return segments



def generate_metadata(symbols, segments):
    """Generate JSON metadata for symbols and segments."""
    unresolved_dependencies = list(
        set(dep for symbol in symbols for dep in symbol.dependencies if dep not in [s.name for s in symbols])
    )
    metadata = {
        "symbols": [s.to_dict() for s in symbols],
        "segments": [s.to_dict() for s in segments],
        "unresolved_dependencies": unresolved_dependencies,
    }
    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved at {metadata_file}")
    return metadata_file


def preprocess(c_file, max_complexity):
    create_output_dirs()

    print("Running the C preprocessor...")
    preprocessed_file = remove_blank_lines(preprocess_with_cpp(c_file))

    print("Processing macros...")
    processed_file, macros_file = process_macros(preprocessed_file)
    processed_file = remove_blank_lines(processed_file)

    print("Extracting contextual information...")
    symbols = extract_contextual_info(processed_file)
    symbols = ensure_unique_namespaces(symbols, processed_file)

    print("Segmenting code...")
    segments = segment_code(processed_file, symbols, max_complexity)

    print("Generating metadata...")
    generate_metadata(symbols, segments)

    print(f"Preprocessing complete. Outputs saved in {OUTPUT_DIR}.")


if __name__ == "__main__":
    input_file = "main.c"
    clang.cindex.Config.set_library_file("/usr/lib/x86_64-linux-gnu/libclang-14.so.14.0.6")
    preprocess(input_file, max_complexity=80)
