import os
import json
from preprocessor.preprocess import (
    preprocess_with_cpp,
    process_macros,
    remove_blank_lines,
    extract_contextual_info,
    dynamic_segment_code,
)


OUTPUT_DIR = "output"

def validate_input_file(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"The input file '{file}' does not exist.")

def create_output_dirs(base_dir="output"):
    """Ensure the output and segment directories exist."""
    output_dir = base_dir
    segment_dir = os.path.join(output_dir, "segments")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(segment_dir, exist_ok=True)
    return output_dir, segment_dir

def generate_metadata(symbols, segments):
    """
    Generate metadata for symbols and segments.
    Args:
        symbols (list): List of extracted symbols.
        segments (list): List of segment file paths.
    Returns:
        str: Path to the metadata JSON file.
    """
    segment_metadata = []

    for idx, segment_file in enumerate(segments):
        # Map contained symbols to their segments
        contained_symbols = [
            s.name for s in symbols
            if os.path.samefile(segment_file, segment_file)
        ]
        dependencies = set(
            dep
            for symbol in symbols
            if symbol.name in contained_symbols
            for dep in symbol.dependencies
        )
        segment_metadata.append({
            "segment_id": idx,
            "file": segment_file,
            "contained_symbols": contained_symbols,
            "dependencies": list(dependencies - set(contained_symbols)),
        })

    metadata = {
        "segments": segment_metadata,
        "unresolved_dependencies": list(
            set(dep for symbol in symbols for dep in symbol.dependencies)
            - {s.name for s in symbols}
        ),
    }

    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved at {metadata_file}")
    return metadata_file

def preprocess_and_segment(input_file, max_complexity, output_dir="output"):
    """
    Perform preprocessing and segmentation on the input C file.
    Args:
        input_file (str): Path to the input C file.
        max_complexity (int): Maximum complexity per segment.
    Returns:
        tuple: List of symbols and list of segment file paths.
    """
    # Ensure output directories exist
    output_dir, segment_dir = create_output_dirs(output_dir)

    # Preprocessing stage
    print("Running the C preprocessor...")
    preprocessed_file = preprocess_with_cpp(input_file, output_dir=output_dir)
    preprocessed_file = remove_blank_lines(preprocessed_file)

    # Macro processing
    print("Processing macros...")
    processed_file = process_macros(preprocessed_file)
    processed_file = remove_blank_lines(preprocessed_file)

    # Context extraction
    print("Extracting contextual information...")
    symbols = extract_contextual_info(processed_file)

    # Dynamic segmentation
    print("Segmenting code dynamically...")
    segments = dynamic_segment_code(processed_file, symbols, max_complexity)

    return symbols, segments

def main(input_file, max_complexity=80, output_dir="output"):
    """
    Main entry point for preprocessing and segmentation.
    Args:
        input_file (str): Path to the input C file.
        max_complexity (int): Maximum complexity per segment.
        output_dir (str): Directory to store outputs.
    """
    try:
        # Validate input file
        validate_input_file(input_file)
        print(f"Resolved input file path: {os.path.abspath(input_file)}")

        print(f"Starting preprocessing for {input_file}...")

        # Preprocess and segment the code
        symbols, segments = preprocess_and_segment(input_file, max_complexity, output_dir)

        # Generate and save metadata
        print("Generating metadata...")
        metadata_file = generate_metadata(symbols, segments)

        print("Preprocessing and segmentation complete.")
        print(f"Outputs saved in '{output_dir}'.")
        print(f"Metadata file: {metadata_file}")

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Error generating metadata: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # User-defined input file and settings
    input_file = "main.c"
    max_complexity = 70
    main(input_file, max_complexity)
