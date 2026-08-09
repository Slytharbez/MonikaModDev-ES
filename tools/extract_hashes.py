#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs

# Define paths
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL_DIR = os.path.join(WORKSPACE_ROOT, "Monika After Story", "game", "tl", "spanish")
IDS_FILE = os.path.join(WORKSPACE_ROOT, "tl_test_ids.txt")

# Set of game variables and pronoun variables to ignore
EXCLUDED_VARIABLES = {
    # MAS standard / game variables
    "player", "m_name", "mas_get_playernickname", "p_nickname", "inputname",
    
    # Spanish pronoun and gender mapping variables from zz_spanish.rpy
    "un_una", "el_la", "lo_la", "uno_una", "el_ella", "cap_el_ella", 
    "al_ala", "del_dela", "hero", "buen_buena", "dormilon_dormilona", 
    "or_ora", "on_ona", "amigo_amiga", "dor_dora", "tores", "e_a", "o_a"
}

def extract_variables_from_line(line):
    """
    Extracts all valid variable names from a Ren'Py line (within brackets like [variable]).
    Ignores variables ending in !t, shorter than 4 characters, or in the exclude list.
    """
    found = []
    # Find everything inside brackets [ ... ]
    tags = re.findall(r'\[([^\]]+)\]', line)
    
    for tag in tags:
        tag = tag.strip()
        # Ignore tags ending in !t
        if tag.endswith("!t") or "!t" in tag:
            continue
            
        # Extract the variable name (before any conversion tag like !c, !u, etc.)
        var_name = tag.split('!')[0].strip()
        
        # Filter by length and ignore lists
        if len(var_name) >= 4 and var_name not in EXCLUDED_VARIABLES:
            found.append(var_name)
            
    return found

def main():
    print("Scanning translation files starting with 'script-' in: " + TL_DIR)
    
    if not os.path.exists(TL_DIR):
        print("Error: Spanish translation directory not found!")
        return
        
    # 1. Load existing hashes from tl_test_ids.txt to avoid duplicate hashes
    existing_hashes = set()
    if os.path.exists(IDS_FILE):
        try:
            with codecs.open(IDS_FILE, "r", "utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        existing_hashes.add(line)
            print("Loaded {} existing hashes from tl_test_ids.txt".format(len(existing_hashes)))
        except Exception as e:
            print("Warning: Could not read existing tl_test_ids.txt: " + str(e))

    # Keep track of variables we have already found
    seen_variables = set()
    hashes_to_add = []
    registered_vars_map = {} # Maps variable -> hash it was found in

    # 2. Scan all files starting with "script-" and ending in ".rpy"
    files_to_scan = [f for f in os.listdir(TL_DIR) if f.startswith("script-") and f.endswith(".rpy")]
    
    for filename in sorted(files_to_scan):
        filepath = os.path.join(TL_DIR, filename)
        
        try:
            with codecs.open(filepath, "r", "utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print("Error reading {}: {}".format(filename, e))
            continue
            
        current_hash = None
        
        for line in lines:
            # Detect translate block start
            # translate spanish greeting_after_bath_98430dea:
            translate_match = re.match(r'^\s*translate\s+spanish\s+(\w+)\s*:', line)
            if translate_match:
                current_hash = translate_match.group(1)
                continue
                
            if current_hash:
                # Find valid variables in this line
                vars_found = extract_variables_from_line(line)
                
                for var in vars_found:
                    if var not in seen_variables:
                        seen_variables.add(var)
                        registered_vars_map[var] = current_hash
                        
                        # Only add the hash if it isn't already in the file
                        if current_hash not in existing_hashes and current_hash not in hashes_to_add:
                            hashes_to_add.append(current_hash)
                            
    # 3. Output results
    print("\n--- EXTRACTION SUMMARY ---")
    print("New variables registered ({}):".format(len(registered_vars_map)))
    for var, hash_id in sorted(registered_vars_map.items()):
        print("  - {} (found in hash: {})".format(var, hash_id))
        
    if hashes_to_add:
        print("\nAdding {} new hashes to tl_test_ids.txt...".format(len(hashes_to_add)))
        try:
            with codecs.open(IDS_FILE, "a", "utf-8") as f:
                # Ensure a newline before appending if file is not empty
                if os.path.exists(IDS_FILE) and os.path.getsize(IDS_FILE) > 0:
                    f.write("\n")
                
                f.write("# --- Automated Extraction of Dialogue Variables ---\n")
                for hash_id in hashes_to_add:
                    f.write(hash_id + "\n")
            print("Done! Hashes successfully appended.")
        except Exception as e:
            print("Error writing to tl_test_ids.txt: " + str(e))
    else:
        print("\nNo new variables or hashes to add.")

if __name__ == "__main__":
    main()
