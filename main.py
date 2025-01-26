import os
import json
from typing import List, Tuple
from preprocessor.preprocess import (
    extract_user_defined_includes,
    preprocess_with_cpp,
    process_macros,
    remove_blank_lines,
    extract_contextual_info,
    dynamic_segment_code,
    filter_segments
)

OUTPUT_DIR = "output"

def validate_input_file(file: str) -> None:
    """
    Validate that the input file exists.
    Args:
        file (str): Path to the input file.
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"The input file '{file}' does not exist.")

def create_output_dirs(base_dir: str = OUTPUT_DIR) -> Tuple[str, str]:
    """
    Ensure the output and segment directories exist.
    Args:
        base_dir (str): Base directory for outputs.
    Returns:
        Tuple[str, str]: Paths to the output and segment directories.
    """
    output_dir = base_dir
    segment_dir = os.path.join(output_dir, "segments")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(segment_dir, exist_ok=True)
    return output_dir, segment_dir

def generate_metadata(symbols: List, segments: List[str]) -> str:
    """
    Generate metadata for symbols and segments.
    Args:
        symbols (list): List of extracted symbols.
        segments (list): List of segment file paths.
    Returns:
        str: Path to the metadata JSON file.
    """
    segment_metadata = []
    # segments = filter_segments(symbols, segments)
    for idx, segment_file in enumerate(segments):
        contained_symbols = [
            s.name for s in symbols
            if s.segment == segment_file
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

    unresolved_dependencies = list(
        set(dep for symbol in symbols for dep in symbol.dependencies)
        - {s.name for s in symbols}
    )

    metadata = {
        "segments": segment_metadata,
        "unresolved_dependencies": unresolved_dependencies,
    }

    metadata_file = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved at {metadata_file}")
    return metadata_file

def preprocess_and_segment(
    input_file: str, max_complexity: int, output_dir: str = OUTPUT_DIR
) -> Tuple[List, List[str]]:
    """
    Perform preprocessing and segmentation on the input C file.
    Args:
        input_file (str): Path to the input C file.
        max_complexity (int): Maximum complexity per segment.
    Returns:
        Tuple[List, List[str]]: List of symbols and segment file paths.
    """
    output_dir, segment_dir = create_output_dirs(output_dir)

    # Preprocessing stage
    print("Running the C preprocessor...")
    user_defined_paths = extract_user_defined_includes(input_file)

    # Step 2: Preprocess the file using only user-defined includes
    preprocessed_file = preprocess_with_cpp(input_file, include_paths=user_defined_paths)
    preprocessed_file = remove_blank_lines(preprocessed_file)

    # Macro processing
    print("Processing macros...")
    processed_file = process_macros(preprocessed_file)
    processed_file = remove_blank_lines(processed_file)

    # Context extraction
    print("Extracting contextual information...")
    symbols = extract_contextual_info(processed_file)

    # Dynamic segmentation
    print("Segmenting code dynamically...")
    segments = dynamic_segment_code(processed_file, symbols)

    return symbols, segments

def main(input_file: str, max_complexity: int = 80, output_dir: str = OUTPUT_DIR) -> None:
    """
    Main entry point for preprocessing and segmentation.
    Args:
        input_file (str): Path to the input C file.
        max_complexity (int): Maximum complexity per segment.
        output_dir (str): Directory to store outputs.
    """
    try:
        validate_input_file(input_file)
        print(f"Resolved input file path: {os.path.abspath(input_file)}")

        print(f"Starting preprocessing for {input_file}...")
        symbols, segments = preprocess_and_segment(input_file, max_complexity, output_dir)

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
        raise

if __name__ == "__main__":
    input_file = "main.c"
    max_complexity = 70
    main(input_file, max_complexity)
