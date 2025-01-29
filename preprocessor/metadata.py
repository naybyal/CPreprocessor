import os
import json

def generate_metadata(symbols, segments, output_dir="output"):
    """Generate metadata linking segments with extracted symbols."""
    os.makedirs(output_dir, exist_ok=True)
    metadata = {"segments": []}

    for idx, segment_file in enumerate(segments):
        contained_symbols = [
            symbol["name"] for symbol in symbols
            if symbol["start_line"] - 1 <= idx < symbol["end_line"]
        ]
        dependencies = set(
            dep for symbol in symbols
            if symbol["name"] in contained_symbols
            for dep in symbol["dependencies"]
        )

        metadata["segments"].append({
            "segment_id": idx,
            "file": segment_file,
            "contained_symbols": contained_symbols,
            "dependencies": list(dependencies - set(contained_symbols)),
        })

    metadata_file = os.path.join(output_dir, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    return metadata_file
