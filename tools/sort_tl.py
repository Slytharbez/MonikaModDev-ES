import os
import re

# --- PATHS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
tl_dir = os.path.join(base_dir, "Monika After Story", "game", "tl", "spanish")

# Matches: # game/screens.rpy:723
comment_re = re.compile(r'^(\s*)# (game/[a-zA-Z0-9_\-\./]+):(\d+)\s*$')

def parse_blocks(lines):
    """
    Splits the file into non-sortable 'text' chunks and sortable 'blocks' chunks.
    A 'blocks' chunk is a list of translation blocks that share the same filepath and indentation.
    """
    chunks = []
    
    current_chunk_type = 'text' # 'text' or 'blocks'
    current_text = []
    current_blocks = []
    
    current_block_lines = []
    current_block_sort_key = None # (filepath, line_num)
    current_block_indent = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        match = comment_re.match(line)
        if match:
            indent = match.group(1)
            filepath = match.group(2)
            lineno = int(match.group(3))
            
            if current_chunk_type == 'text':
                if current_text:
                    chunks.append(('text', current_text))
                    current_text = []
                
                current_chunk_type = 'blocks'
                current_block_lines = [line]
                current_block_sort_key = (filepath, lineno)
                current_block_indent = indent
            else:
                # We are already in 'blocks' mode
                prev_filepath = current_block_sort_key[0]
                
                # Check if this new block belongs to the same file group and has the same indentation
                if filepath == prev_filepath and indent == current_block_indent:
                    # Save the previous block in the current group
                    current_blocks.append({
                        'lines': current_block_lines,
                        'key': current_block_sort_key,
                    })
                    # Start a new block
                    current_block_lines = [line]
                    current_block_sort_key = (filepath, lineno)
                else:
                    # The group broke (different file or indentation). 
                    # Save the previous block, close the blocks chunk, and start a new blocks chunk
                    current_blocks.append({
                        'lines': current_block_lines,
                        'key': current_block_sort_key,
                    })
                    chunks.append(('blocks', current_blocks))
                    
                    current_blocks = []
                    current_block_lines = [line]
                    current_block_sort_key = (filepath, lineno)
                    current_block_indent = indent
        else:
            if current_chunk_type == 'text':
                current_text.append(line)
            else:
                current_block_lines.append(line)
                
        i += 1

    # Save any remaining data at the end of the file
    if current_chunk_type == 'text' and current_text:
        chunks.append(('text', current_text))
    elif current_chunk_type == 'blocks':
        if current_block_lines:
            current_blocks.append({
                'lines': current_block_lines,
                'key': current_block_sort_key,
            })
        if current_blocks:
            chunks.append(('blocks', current_blocks))

    return chunks

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return False
        
    orig_count = len(lines)
    chunks = parse_blocks(lines)
    
    new_lines = []
    modified = False
    
    for ctype, content in chunks:
        if ctype == 'text':
            new_lines.extend(content)
        elif ctype == 'blocks':
            # Sort the group of blocks by line number (the second element of the key)
            sorted_blocks = sorted(content, key=lambda b: b['key'][1])
            
            original_order = [b['key'][1] for b in content]
            sorted_order = [b['key'][1] for b in sorted_blocks]
            
            if original_order != sorted_order:
                modified = True
                
            for b in sorted_blocks:
                new_lines.extend(b['lines'])
                
    new_count = len(new_lines)
    
    # SAFETY VERIFICATION: Ensure the line count exactly matches
    if new_count != orig_count:
        print(f"[ERROR] {os.path.basename(filepath)} line count mismatch! Orig: {orig_count}, New: {new_count}. Skipped.")
        return False
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"[SORTED] {os.path.basename(filepath)}")
        return True
        
    return False

def main():
    print(f"Sorting files in {tl_dir} ...")
    print("-" * 50)
    
    count = 0
    for root, dirs, files in os.walk(tl_dir):
        for file in files:
            if file.endswith(".rpy"):
                if process_file(os.path.join(root, file)):
                    count += 1
                    
    print("-" * 50)
    print(f"Completed! {count} files were successfully sorted.")

if __name__ == "__main__":
    main()
