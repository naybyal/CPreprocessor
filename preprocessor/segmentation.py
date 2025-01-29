import os
import json
import clang.cindex
import networkx as nx

def extract_symbols(file):
    """Extract function definitions, structs, and macros using Clang AST."""
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    symbols = []

    def traverse(cursor):
        if cursor.kind in (
            clang.cindex.CursorKind.FUNCTION_DECL,
            clang.cindex.CursorKind.STRUCT_DECL,
            clang.cindex.CursorKind.UNION_DECL,
            clang.cindex.CursorKind.MACRO_DEFINITION,
        ):
            symbols.append({
                "name": cursor.spelling,
                "kind": cursor.kind.name,
                "start_line": cursor.extent.start.line,
                "end_line": cursor.extent.end.line,
                "dependencies": [ref.spelling for ref in cursor.get_children() if ref.kind.is_reference()]
            })
        for child in cursor.get_children():
            traverse(child)

    traverse(translation_unit.cursor)
    return symbols

def build_dependency_graph(symbols):
    """Build a dependency graph using function calls and struct references."""
    graph = nx.DiGraph()
    for symbol in symbols:
        graph.add_node(symbol["name"])
        for dependency in symbol["dependencies"]:
            graph.add_edge(symbol["name"], dependency)
    return graph

def segment_code(file, symbols, output_dir="output"):
    """Segment code based on extracted symbols."""
    os.makedirs(output_dir, exist_ok=True)
    with open(file, "r") as f:
        lines = f.readlines()

    segments = []
    for idx, symbol in enumerate(symbols):
        start, end = symbol["start_line"] - 1, symbol["end_line"]
        if start < 0 or end > len(lines):
            continue

        segment_file = os.path.join(output_dir, f"segment_{idx}.c")
        with open(segment_file, "w") as f:
            f.writelines(lines[start:end])
        segments.append(segment_file)

    return segments
