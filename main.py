import os
import logging
from preprocessor.preprocess import preprocess_c_file
from preprocessor.segmentation import extract_symbols, build_dependency_graph, segment_code
from preprocessor.metadata import generate_metadata

OUTPUT_DIR = "output"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def main(input_file):
    logging.info("Preprocessing C file...")
    preprocessed_file = preprocess_c_file(input_file)

    logging.info("Extracting symbols...")
    symbols = extract_symbols(preprocessed_file)

    logging.info("Building dependency graph...")
    dependency_graph = build_dependency_graph(symbols)

    logging.info("Segmenting code...")
    segments = segment_code(preprocessed_file, symbols)

    logging.info("Generating metadata...")
    metadata_file = generate_metadata(symbols, segments)

    logging.info(f"Preprocessing complete. Segments stored in {OUTPUT_DIR}")
    logging.info(f"Metadata file saved at {metadata_file}")

if __name__ == "__main__":
    input_file = "main.c"
    main(input_file)
