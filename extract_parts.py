import os
import re

models_dir = 'models'
output_dir = 'ldraw_parts'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def extract_from_mpd(mpd_path):
    print(f"Scanning {mpd_path}...")
    with open(mpd_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split by "0 FILE"
    # Regex to find "0 FILE filename"
    # The content of the file follows until the next "0 FILE" or end of file.
    
    # We can iterate line by line to be safer.
    current_file = None
    current_content = []
    
    lines = content.splitlines()
    for line in lines:
        if line.startswith('0 FILE '):
            # Save previous file if exists
            if current_file:
                save_file(current_file, current_content)
            
            # Start new file
            parts = line.split()
            if len(parts) >= 3:
                current_file = ' '.join(parts[2:]) # Handle filenames with spaces if any
                current_content = []
                # We don't include the "0 FILE" line in the .dat file usually, 
                # but LDraw tools might expect it? 
                # Standard .dat files don't start with "0 FILE".
                # They start with "0 Name: ..." usually.
                # The "0 FILE" is the MPD delimiter.
        elif line.startswith('0 NOFILE'):
             if current_file:
                save_file(current_file, current_content)
                current_file = None
                current_content = []
        else:
            if current_file:
                current_content.append(line)
    
    # Save last file
    if current_file:
        save_file(current_file, current_content)

def save_file(filename, content_lines):
    # We only care about .dat files for now, maybe .ldr too?
    # The user wants parts, which are usually .dat.
    if not filename.lower().endswith('.dat'):
        return

    # Handle subdirectories in filenames like "s/3005s01.dat"
    # We should probably flatten them or respect them?
    # The repo structure has `ldraw_parts/s/`, so we should respect it.
    
    # Normalize path separators
    filename = filename.replace('\\', '/')
    
    full_path = os.path.join(output_dir, filename)
    
    # Create subdirectories if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Write file
    # We overwrite existing files to ensure we have the version from the MPD 
    # (which might be the one the user expects, or maybe not? 
    # Let's only write if not exists to avoid breaking existing valid parts, 
    # OR overwrite if the existing one is empty/broken?
    # User said "hunt down missing parts", so let's prioritize filling gaps.
    if not os.path.exists(full_path):
        print(f"Extracting {filename}")
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))
    else:
        # Optional: Check if existing file is smaller/broken?
        # For now, skip existing.
        pass

# Scan all MPD files
for root, dirs, files in os.walk(models_dir):
    for file in files:
        if file.lower().endswith('.mpd'):
            extract_from_mpd(os.path.join(root, file))

print("Extraction complete.")
