import re

def parse_macros(file_path):
    macro_constants = []
    macro_functions = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # Match constant macros
        const_match = re.match(r"^#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.*)$", line)
        if const_match:
            macro_constants.append({
                "name": const_match.group(1),
                "value": const_match.group(2)
            })
            continue
        
        # Match function-like macros
        func_match = re.match(r"^#define\s+([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)\s+(.*)$", line)
        if func_match:
            macro_functions.append({
                "name": func_match.group(1),
                "args": func_match.group(2).split(','),
                "body": func_match.group(3)
            })
    
    return macro_constants, macro_functions


constants, functions = parse_macros("main.c")

print("Constants:")
for const in constants:
    print(f"{const['name']} = {const['value']}")

print("\nFunctions:")
for func in functions:
    print(f"{func['name']}({', '.join(func['args'])}) = {func['body']}")
