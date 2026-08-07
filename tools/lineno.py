import os
import re

# --- CONFIGURATION ---
# Range of lines to search above and below the original line (fallback)
SEARCH_MARGIN = 500 

# Files and directories to exclude
EXCLUDE_FILES = ["zz_poems.rpy", "script-poems.rpy"]
EXCLUDE_DIRS = ["dev"]

# --- PATHS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
game_dir = os.path.join(base_dir, "Monika After Story", "game")
tl_dir = os.path.join(game_dir, "tl", "spanish")

# --- REGEXES ---
# Matches: # game/chess.rpy:3526
comment_re = re.compile(r'^(\s*)# (game/[a-zA-Z0-9_\-\./]+):(\d+)\s*$')
# Matches commented original dialogue text: # m 1eua "Hello" -> extracts 'm 1eua "Hello"'
dialogue_re = re.compile(r'^\s*#\s+(.*?\".*\")')
# Matches old string translation blocks: old "Hello" -> extracts "Hello"
old_re = re.compile(r'^\s*old\s+\"(.*)\"')

def find_line_in_file(filepath, search_text, expected_line, last_found_lines, margin=SEARCH_MARGIN):
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return None
        
    last_line = last_found_lines.get(filepath, 0)
    
    # Normalize whitespaces to prevent failures on double spaces
    def clean(t):
        return re.sub(r'\s+', ' ', t).strip()
        
    cleaned_search = clean(search_text)
    
    # 1st Pass: Search sequentially AFTER the last found line to handle identical duplicates correctly
    if last_line > 0:
        start_idx = last_line
        end_idx = min(len(lines), start_idx + margin)
        
        for i in range(start_idx, end_idx):
            if cleaned_search in clean(lines[i]):
                last_found_lines[filepath] = i + 1
                return i + 1

    # 2nd Pass (Fallback): Search around the expected_line within the margin
    start_idx = max(0, expected_line - margin - 1)
    end_idx = min(len(lines), expected_line + margin)
    
    for i in range(start_idx, end_idx):
        if cleaned_search in clean(lines[i]):
            last_found_lines[filepath] = i + 1
            return i + 1
            
    return None

def process_tl_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return
        
    modified = False
    last_found_lines = {}
    
    i = 0
    while i < len(lines):
        match = comment_re.match(lines[i])
        if match:
            indent = match.group(1)
            orig_rel_path = match.group(2)
            orig_line = int(match.group(3))
            
            if orig_rel_path.startswith("game/"):
                rel_path = orig_rel_path[5:]
                orig_abs_path = os.path.join(game_dir, rel_path)
            else:
                orig_abs_path = os.path.join(base_dir, "Monika After Story", orig_rel_path)
            
            search_text = None
            j = i + 1
            while j < min(i + 5, len(lines)):
                if lines[j].strip().startswith("translate "):
                    j += 1
                    continue
                    
                diag_match = dialogue_re.match(lines[j])
                if diag_match:
                    search_text = diag_match.group(1)
                    break
                    
                old_match = old_re.match(lines[j])
                if old_match:
                    search_text = old_match.group(1)
                    break
                    
                j += 1
                
            if search_text and len(search_text) > 2:
                new_line = find_line_in_file(orig_abs_path, search_text, orig_line, last_found_lines, margin=SEARCH_MARGIN)
                
                if new_line and new_line != orig_line:
                    lines[i] = f"{indent}# {orig_rel_path}:{new_line}\n"
                    modified = True
                    print(f"[{os.path.basename(filepath)}] Updated {orig_rel_path} : {orig_line} -> {new_line}")
        i += 1
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

def main():
    print(f"Scanning in {tl_dir} ...")
    print("-" * 50)
    
    for root, dirs, files in os.walk(tl_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith(".rpy") and file not in EXCLUDE_FILES:
                process_tl_file(os.path.join(root, file))
                
    print("-" * 50)
    print("Completed!")

if __name__ == "__main__":
    main()
