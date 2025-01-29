import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def read_metadata(metadata_file):
    """Reads metadata.json to get segment details."""
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    return metadata["segments"]

def read_segment(file_path):
    """Reads a segment C file."""
    with open(file_path, "r") as f:
        return f.read()



def translate_to_rust(c_code):
    """Translates C code to Rust using Gemini API."""
    try:
        # Configure the Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Create the model instance
        model = genai.GenerativeModel('gemini-pro')
        
        # Create the system instruction prompt
        prompt = f"""You are an expert programmer experienced in C and Rust conversion as per 2025 standards.
        Please translate the following C code to safe, idiomatic Rust code.

        Requirements:

       Requirements:
        1. Use proper ownership semantics
        2. Convert pointers to Rust-safe constructs
        3. Add proper error handling
        4. Preserve original functionality
        5. Do not include ANY comments or explanations
        6. Do not expand stray function calls (segments will be merged)
        7. Output ONLY the Rust code with no additional text
        
                
        C Code:
        {c_code}
        
        Rust Translation:"""
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Extract the Rust code portion from the response
        rust_code = extract_rust_code(response.text)
        return rust_code
        
    except Exception as e:
        return f"// Translation failed: {str(e)}"

def extract_rust_code(response_text):
    """Extracts clean Rust code from API response."""
    rust_code = response_text.strip()
    
    # Remove code block markers
    if rust_code.startswith("```rust"):
        rust_code = rust_code[len("```rust"):]
    elif rust_code.startswith("```"):
        rust_code = rust_code[len("```"):]
    
    if rust_code.endswith("```"):
        rust_code = rust_code[:-len("```")]
    
    rust_code = rust_code.strip()
    
    # Filter out comment lines and empty lines
    cleaned_lines = []
    for line in rust_code.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def process_segments(metadata_file):
    """Processes metadata and translates segments to Rust."""
    segments = read_metadata(metadata_file)
    
    translated_segments = {}

    for segment in segments:
        c_code = read_segment(segment["file"])
        rust_code = translate_to_rust(c_code)
        translated_segments[segment["segment_id"]] = rust_code

    return translated_segments

# if __name__ == "__main__":
#     metadata_file = "metadata.json"
#     rust_segments = process_segments(metadata_file)

#     for segment_id, rust_code in rust_segments.items():
#         print(f"\n===== {segment_id}.rs =====\n")
#         print(rust_code)