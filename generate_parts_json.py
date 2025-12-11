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

# Whitelist of parts to include (based on the provided image)
WHITELIST = {
    # Bricks (Standard)
    '3005', '3004', '3622', '3010', '3009', '3008', '3007', '3006', # 1x1 to 2x10
    '3003', '3002', '3001', '2456', # 2x2 to 2x6
    '2357', # 2x2 Corner
    
    # Plates (Standard)
    '3024', '3023', '3623', '3710', '3666', '3460', # 1x1 to 1x8
    '3022', '3021', '3020', '3795', '3832', '2445', # 2x2 to 2x12
    '3031', '3032', '3034', '3036', '41539', # 4x4, 4x6, 2x8, 6x8, 8x8
    '2420', # 2x2 Corner
    
    # Tiles (Standard)
    '3070b', '3069b', '3068b', '2431',
    
    # Slopes (Classic 45 and 33)
    '3040b', '3039', # 45 2x1, 2x2
    '3665', '3660', # Inv 45 2x1, 2x2
    '3045', '3046', # Corner
    '3298', '3297', # 33 3x2, 3x4
    '3038', # 45 2x3
    '4286', # 33 3x1
    '3676', # Inv 45 2x2 Corner
    '3675', # 33 3x3 Corner
    '3044', '3043', # 45 Double
    
    # Rounds (Classic)
    '4073', '3062b', '6141', '3941', '4589', '3942b', # 1x1 Plate, 1x1 Brick, 1x1 Plate Round, 2x2 Brick Round, Cones
    
    # Arches (Classic)
    '3659', '6091', '4490',
    
    # SNOT (Vintage only)
    '4070', # Headlight Brick (1980)
    
    # Modified (Classic)
    '3794b', # Jumper Plate
    '2412b', # Grille Tile
    '4085c' # Clip Plate
}

# Only look at the root directory to avoid primitives in subfolders (s/, 48/, 8/)
for file in os.listdir(parts_dir):
    full_path = os.path.join(parts_dir, file)
    if os.path.isfile(full_path) and file.lower().endswith('.dat'):
        # Check if part is in whitelist
        part_name = os.path.splitext(file)[0].lower()
        if part_name not in WHITELIST:
            continue

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
