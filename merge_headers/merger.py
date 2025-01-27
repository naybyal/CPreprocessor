def merge_includes(file_path, include_dirs):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    merged_content = []
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith("#include"):
            # Check for double-quoted includes
            if '"' in line:
                try:
                    header_name = line.split('"')[1]
                    for include_dir in include_dirs:
                        try:
                            # Open and read the included header file
                            with open(f"{include_dir}/{header_name}", 'r') as header_file:
                                # Ensure a newline is added after including header content
                                merged_content.extend(header_file.readlines())
                                if not header_file.readlines()[-1].endswith("\n"):
                                    merged_content.append("\n")
                            break  # Stop searching once the file is found
                        except FileNotFoundError:
                            continue
                except IndexError:
                    print(f"Malformed include directive: {line}")
            else:
                # Skip system includes (e.g., <stdio.h>)
                print(f"Skipping system include: {line}")
        else:
            merged_content.append(line + "\n")
    
    return merged_content


def main():
    # Input file and include directories
    source_file = "merge_headers/main.c"
    include_dirs = ["merge_headers/includes", "/usr/include", "/usr/local/include"]
    
    # Merge the includes
    try:
        merged_content = merge_includes(source_file, include_dirs)
        
        # Output file for the merged content
        output_file = "merge_headers/merged_main.c"
        with open(output_file, 'w') as f:
            f.writelines(merged_content)
        
        print(f"Merged content written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()