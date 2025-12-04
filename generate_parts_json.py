import os
import json

parts_dir = 'ldraw_parts'
unofficial_dir = 'ldraw_unofficial'
parts = []

# Cache of existing files to avoid repeated disk access
existing_files = set()
for root, dirs, files in os.walk(parts_dir):
    for file in files:
        # Store relative path from parts_dir/.. (workspace root) would be ideal, 
        # but LDraw references are usually just filenames or relative paths like s/file.dat
        # Let's store just the filename for simple check, and relative path for subfolders.
        
        # Actually, LDraw references are case-insensitive.
        # If a file is in ldraw_parts/s/3001s01.dat, it is referenced as s/3001s01.dat
        
        rel_path = os.path.relpath(os.path.join(root, file), parts_dir)
        existing_files.add(rel_path.lower().replace('\\', '/'))
        existing_files.add(file.lower()) # Also add just filename for root files

for root, dirs, files in os.walk(unofficial_dir):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), unofficial_dir)
        existing_files.add(rel_path.lower().replace('\\', '/'))
        existing_files.add(file.lower())

def check_dependencies(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith('1 '):
                    parts = line.split()
                    if len(parts) >= 15:
                        # The last part is the filename, but it might contain spaces? 
                        # LDraw filenames usually don't have spaces, but let's be careful.
                        # Actually, the format is fixed. The filename is the last token(s).
                        # But usually it's just one token.
                        ref_file = ' '.join(parts[14:])
                        ref_file_lower = ref_file.lower().replace('\\', '/')
                        
                        # Check if this referenced file exists
                        if ref_file_lower not in existing_files:
                            # Some primitives might be internal or generated?
                            # But 4592.dat is definitely a missing part.
                            # Primitives like 'stud.dat' should be in the list.
                            return False, ref_file
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False, "Read Error"
    return True, None

# Only look at the root directory to avoid primitives in subfolders (s/, 48/, 8/)
for file in os.listdir(parts_dir):
    full_path = os.path.join(parts_dir, file)
    if os.path.isfile(full_path) and file.lower().endswith('.dat'):
        # Check dependencies
        valid, missing = check_dependencies(full_path)
        if valid:
            parts.append(file)
        else:
            print(f"Skipping {file} due to missing dependency: {missing}")

# Sort parts for better UX
parts.sort()

with open('parts.json', 'w') as f:
    json.dump(parts, f)

print(f"Generated parts.json with {len(parts)} parts.")
