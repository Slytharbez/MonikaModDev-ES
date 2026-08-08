# Translation Testing Tool by Hash
# Created by Antigravity

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_translation_tester",
            category=["dev"],
            prompt=_("TEST TRANSLATION"),
            pool=True,
            unlocked=True
        )
    )

label dev_translation_tester:
    m 1eua "Starting translation hash testing..."
    python:
        import os
        import re
        import codecs
        
        filepath = os.path.join(renpy.config.basedir, "tl_test_ids.txt")
        debug_filepath = os.path.join(renpy.config.basedir, "translation_tester_debug.log")
        
        debug_log = []
        def log_debug(msg):
            debug_log.append(msg)
            try:
                # Also output to the developer console log
                print("[TL TESTER] " + msg)
            except Exception:
                pass
                
        log_debug("=== TRANSLATION TESTER RUN STARTED ===")

        # Candidate paths to search for the .rpy file
        def resolve_missing_variable(filename, linenumber, var_name):
            log_debug("Resolving variable '" + var_name + "' from file: " + str(filename) + ", line: " + str(linenumber))
            if not filename:
                log_debug("  Error: No filename provided.")
                return None
                
            # Candidate paths to search for the .rpy file
            paths_to_try = []
            
            # 1. Path relative to renpy.config.basedir
            if os.path.isabs(filename):
                paths_to_try.append(filename)
            else:
                paths_to_try.append(os.path.join(renpy.config.basedir, filename))
                
            # 2. Path relative to renpy.config.gamedir
            paths_to_try.append(os.path.join(renpy.config.gamedir, os.path.basename(filename)))
            
            target_path = None
            for path in paths_to_try:
                normalized_path = os.path.abspath(path).replace("\\", "/")
                log_debug("  Checking path: " + normalized_path)
                if os.path.exists(normalized_path):
                    target_path = normalized_path
                    log_debug("  Found file at: " + target_path)
                    break
                    
            if not target_path:
                log_debug("  Error: File does not exist at any searched path.")
                return None
                
            try:
                with codecs.open(target_path, "r", "utf-8") as f:
                    lines = f.readlines()
                log_debug("  Successfully read file. Total lines: " + str(len(lines)))
            except Exception as e:
                log_debug("  Error reading file: " + str(e))
                return None
                
            # Scan backwards starting from before the statement line (0-indexed)
            start_idx = min(linenumber - 1, len(lines) - 1)
            end_idx = max(0, start_idx - 150) # scan up to 150 lines back
            log_debug("  Scanning backward from line index " + str(start_idx) + " to " + str(end_idx))
            
            # Pattern: matches $ var_name = ... or var_name = ...
            pattern = re.compile(r'^\s*(?:\$\s*)?' + re.escape(var_name) + r'\s*=\s*(.+)$')
            
            for i in range(start_idx, end_idx - 1, -1):
                line = lines[i].strip()
                match = pattern.match(line)
                if match:
                    expression = match.group(1).strip()
                    log_debug("  Matched assignment on line " + str(i+1) + ": " + line)
                    log_debug("  Expression to evaluate: " + expression)
                    
                    # 1. Try to evaluate dynamically in the renpy.store scope
                    try:
                        val = eval(expression, renpy.store.__dict__)
                        log_debug("  Successfully evaluated expression. Value: " + str(val))
                        return val
                    except Exception as e:
                        log_debug("  Dynamic evaluation failed: " + str(e))
                        
                    # 2. Regex fallback: Find translate marks like _("something")
                    string_matches = re.findall(r'_\(["\'](.*?)["\']\)', expression)
                    if string_matches:
                        log_debug("  Regex fallback found string_matches: " + str(string_matches))
                        translated_options = [renpy.translation.translate_string(s) for s in string_matches]
                        resolved = "/".join(translated_options)
                        log_debug("  Resolved via regex fallback: " + resolved)
                        return resolved
                        
                    # 3. Regex fallback 2: Find regular strings "something"
                    string_matches_raw = re.findall(r'["\'](.*?)["\']', expression)
                    if string_matches_raw:
                        log_debug("  Regex fallback 2 found string_matches: " + str(string_matches_raw))
                        translated_options = [renpy.translation.translate_string(s) for s in string_matches_raw]
                        resolved = "/".join(translated_options)
                        log_debug("  Resolved via regex fallback 2: " + resolved)
                        return resolved
                        
            log_debug("  Variable '" + var_name + "' assignment not found within 150 lines backward.")
            return None

        # Read active test IDs
        if not os.path.exists(filepath):
            log_debug("Error: File tl_test_ids.txt not found at: " + filepath)
            renpy.say(m, "Error: File tl_test_ids.txt not found in the game's root directory.")
            ids = []
        else:
            try:
                with codecs.open(filepath, "r", "utf-8") as f:
                    lines = f.readlines()
                
                ids = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        ids.append(line)
                log_debug("Loaded test IDs: " + str(ids))
            except Exception as e:
                log_debug("Error reading tl_test_ids.txt: " + str(e))
                renpy.say(m, "Error reading file: " + str(e))
                ids = []
                
        if not ids:
            renpy.say(m, "No valid hashes found to test in tl_test_ids.txt.")
            
        translator = renpy.game.script.translator
        
        for identifier in ids:
            log_debug("--- Processing Hash: " + identifier + " ---")
            
            # 1. Verify if the hash exists in the original game script
            if identifier not in translator.default_translates:
                log_debug("Hash '" + identifier + "' does not exist in translator.default_translates.")
                renpy.say(m, "Hash '" + identifier + "' does not exist in the game scripts.")
                continue
                
            # 2. Get the node corresponding to the active translation language
            node = translator.lookup_translate(identifier)
            
            if node is None:
                log_debug("Node returned by lookup_translate is None.")
                renpy.say(m, "No dialogue node found for hash '" + identifier + "'.")
                continue
                
            log_debug("Node details: Type=" + type(node).__name__ + ", filename=" + str(getattr(node, 'filename', None)) + ", linenumber=" + str(getattr(node, 'linenumber', None)))
            
            # 3. Get file and line information from default translation block for variable scanning
            original_node = translator.default_translates.get(identifier, None)
            filename = original_node.filename if original_node else None
            linenumber = original_node.linenumber if original_node else 1
            log_debug("Original node details: Type=" + type(original_node).__name__ + ", filename=" + str(filename) + ", linenumber=" + str(linenumber))
            
            # 4. If the node is a Say dialogue node
            if isinstance(node, renpy.ast.Say):
                who_str = node.who
                what_str = node.what
                interact = node.interact
                attributes = node.attributes
                log_debug("Say Node: who=" + str(who_str) + ", what=\"" + str(what_str) + "\", attributes=" + str(attributes))
                
                # Resolve who is speaking
                who_obj = None
                if who_str:
                    try:
                        who_obj = eval(who_str, globals(), renpy.store.__dict__)
                    except Exception as e:
                        log_debug("Failed to resolve character who_str: " + str(e))
                        who_obj = m
                else:
                    who_obj = m
                    
                # Look for local variables missing from renpy.store and resolve them
                vars_in_text = re.findall(r'\[(\w+?)(?:![\w]+)?\]', what_str)
                log_debug("Variables found in dialogue string: " + str(vars_in_text))
                placeholders = {}
                for var in vars_in_text:
                    if not hasattr(renpy.store, var):
                        log_debug("Variable '" + var + "' is not present in renpy.store. Attempting resolution...")
                        # Try to resolve the variable value dynamically from script
                        resolved_val = resolve_missing_variable(filename, linenumber, var)
                        if resolved_val is not None:
                            log_debug("Successfully set '" + var + "' to: " + str(resolved_val))
                            setattr(renpy.store, var, resolved_val)
                        else:
                            # Fallback placeholder if not found
                            log_debug("Resolution failed for '" + var + "'. Setting fallback placeholder.")
                            setattr(renpy.store, var, "<" + var + ">")
                        placeholders[var] = True
                    else:
                        log_debug("Variable '" + var + "' already exists in renpy.store with value: " + str(getattr(renpy.store, var)))
                        
                # Apply pose/expression attributes if defined
                if attributes:
                    renpy.game.context().say_attributes = attributes
                    
                try:
                    renpy.say(who_obj, what_str, interact=interact)
                finally:
                    # Restore context attributes and clean up temporary store placeholders
                    renpy.game.context().say_attributes = None
                    for var in placeholders:
                        delattr(renpy.store, var)
                        
            # 5. If the node is a Python statement node in the translation block
            elif isinstance(node, renpy.ast.Python):
                log_debug("Executing Python node...")
                renpy.say(m, "[Running translation Python block for " + identifier + "]")
                try:
                    node.execute()
                except Exception as e:
                    log_debug("Python execution failed: " + str(e))
                    renpy.say(m, "Error executing Python block: " + str(e))
            else:
                log_debug("Unsupported statement node: " + type(node).__name__)
                renpy.say(m, "[Unsupported statement node type (" + type(node).__name__ + ") for hash " + identifier + "]")
                
        # Write debug logs to file
        log_debug("=== TRANSLATION TESTER RUN FINISHED ===")
        try:
            with codecs.open(debug_filepath, "w", "utf-8") as f:
                for line in debug_log:
                    f.write(line + "\n")
        except Exception as e:
            renpy.say(m, "Error saving debug log: " + str(e))
                
    m 1hua "Translation testing finished successfully."
    return
