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
        import textwrap
        
        filepath = os.path.join(renpy.config.basedir, "tl_test_ids.txt")
        debug_filepath = os.path.join(renpy.config.basedir, "translation_tester_debug.log")
        output_filepath = os.path.join(renpy.config.basedir, "tl_test_dialogue_output.txt")
        
        debug_log = []
        dialogue_output_log = []
        def log_debug(msg):
            debug_log.append(msg)
            try:
                # Also output to the developer console log
                print("[TL TESTER] " + msg)
            except Exception:
                pass
                
        # Definición segura de resolutores de variables
        def resolve_missing_variable_safely(filename, linenumber, var_name):
            # Builtins
            if var_name in __builtins__:
                return __builtins__[var_name]
                
            log_debug("  Resolving variable '" + var_name + "' from file: " + str(filename) + ", line: " + str(linenumber))
            
            # --- Categoría 5: Funciones y persistencias especiales de MAS ---
            # Si el jugador no tiene seteados valores de cabello/ojos en el persistente de prueba, los inicializamos con valores coherentes en español
            if not getattr(persistent, "_mas_pm_eye_color", None):
                persistent._mas_pm_eye_color = "brown"
            if not getattr(persistent, "_mas_pm_hair_color", None):
                persistent._mas_pm_hair_color = "brown"
            if not getattr(persistent, "_mas_pm_hair_length", None):
                persistent._mas_pm_hair_length = "short"

            # --- Categoría 2: Fechas del Calendario y Variables Dinámicas del Juego ---
            try:
                import datetime
                import store
                if var_name == "todays_date":
                    val, _ = store.mas_calendar.genFormalDispDate(datetime.date.today())
                    return val
                elif var_name == "one_year_later":
                    val, _ = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(), 1))
                    return val
                elif var_name == "one_year_earlier":
                    val, _ = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(), -1))
                    return val
                elif var_name in ["first_sesh", "new_first_sesh"]:
                    # Usar fecha de hoy como fallback de simulación
                    val, _ = store.mas_calendar.genFormalDispDate(datetime.date.today())
                    return val
                elif var_name == "first_sesh_raw":
                    return datetime.date.today()
                elif var_name == "first_sesh_formal":
                    d = datetime.date.today()
                    return " ".join([d.strftime("%B"), store.mas_calendar._formatDay(d.day) + ",", str(d.year)])
                elif var_name in ["bday_str", "new_bday_str"]:
                    val, _ = store.mas_calendar.genFormalDispDate(datetime.date.today())
                    return val
                elif var_name == "wb_quip":
                    import store
                    if hasattr(store, "mas_brbs") and hasattr(store.mas_brbs, "get_wb_quip"):
                        return store.mas_brbs.get_wb_quip()
            except Exception as e:
                log_debug("  Failed Category 2 resolution: " + str(e))

            # --- Categoría 3: Variables de Selección Aleatoria (Quips / Listas) ---
            var_lower = var_name.lower()
            if "quip" in var_lower or "line" in var_lower or "game_name" in var_lower or "ntext" in var_lower or "option" in var_lower:
                # Intentamos buscar si existe la lista correspondiente en renpy.store (ej: gaming_quips)
                possible_list_name = var_name + "s"
                if hasattr(renpy.store, possible_list_name):
                    lst = getattr(renpy.store, possible_list_name)
                    if lst and isinstance(lst, list):
                        return renpy.translation.translate_string(lst[0])
                # Buscar listas de quips conocidas en el store
                for lst_name in ["gaming_quips", "missed_quip_dis_list", "missed_quip_long_list", "missed_quip_short_list", "missed_quip_upset_long_list", "missed_quip_upset_short_list", "d25_gift_quips", "reload_quip_good", "reload_quip_normal", "story_begin_quips", "daydream_quips_enamplus"]:
                    if hasattr(renpy.store, lst_name) and var_name in lst_name:
                        lst = getattr(renpy.store, lst_name)
                        if lst and isinstance(lst, list):
                            return renpy.translation.translate_string(lst[0])
                # Category 3 no longer needs its own mock_fallbacks, it relies on Category 6 now.
                pass

            # --- Categoría 1: Asignaciones de texto directo en el archivo (Regex) ---
            if filename:
                paths_to_try = []
                if os.path.isabs(filename):
                    paths_to_try.append(filename)
                else:
                    paths_to_try.append(os.path.join(renpy.config.basedir, filename))
                paths_to_try.append(os.path.join(renpy.config.gamedir, os.path.basename(filename)))
                
                target_path = None
                for path in paths_to_try:
                    normalized_path = os.path.abspath(path).replace("\\", "/")
                    if os.path.exists(normalized_path):
                        target_path = normalized_path
                        break
                        
                if target_path:
                    try:
                        with codecs.open(target_path, "r", "utf-8") as f:
                            file_lines = f.readlines()
                        
                        # Escanear hacia atrás desde la línea aproximada
                        start_idx = min(linenumber - 1, len(file_lines) - 1)
                        end_idx = max(0, start_idx - 150)
                        
                        pattern = re.compile(r'^\s*(?:\$\s*)?' + re.escape(var_name) + r'\s*=\s*(.+)$')
                        for i in range(start_idx, end_idx - 1, -1):
                            line = file_lines[i].strip()
                            match = pattern.match(line)
                            if match:
                                expression = match.group(1).strip()
                                # Extraer texto plano entre comillas si es directo
                                str_match = re.search(r'(["\'])(.*?)\1', expression)
                                if str_match:
                                    extracted_str = str_match.group(2)
                                    # Traducir si está marcado con _()
                                    if "_(" in expression:
                                        return renpy.translation.translate_string(extracted_str)
                                    return extracted_str
                                    
                                # Si no es texto directo, verificar si es una selección aleatoria de una lista/tupla (ej. random.choice)
                                choice_match = re.search(r'(?:renpy\.)?random\.choice\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', expression)
                                if choice_match:
                                    list_name = choice_match.group(1)
                                    file_content = "".join(file_lines)
                                    list_def_match = re.search(r'\b' + re.escape(list_name) + r'\s*=\s*[\[\(]', file_content)
                                    if list_def_match:
                                        start_pos = list_def_match.end()
                                        search_area = file_content[start_pos:start_pos+500]
                                        # Buscar la primera cadena traducible _("...") en el bloque de la lista
                                        str_in_list_match = re.search(r'_\(\s*(["\'])(.*?)\1\s*\)', search_area, re.DOTALL)
                                        if str_in_list_match:
                                            raw_str = str_in_list_match.group(2)
                                            return renpy.translation.translate_string(raw_str)
                    except Exception as e:
                        log_debug("  Error reading file in Category 1: " + str(e))

            # --- Categoría 6: Fallbacks realistas consolidados para variables no capturadas ---
            if var_name == "curr_year": return 2026 # Debe ser int para evitar crasheos matemáticos

            mock_fallbacks = {
                "gaming_quip": "jugando Super Smash Bros",
                "cb_line": "te extrañé un montón",
                "missed_quip_dis": "gracias por el cumplido",
                "missed_quip_long": "eres muy dulce por decir eso",
                "missed_quip_short": "gracias, Pablo",
                "missed_quip_upset_long": "no estoy de humor para cumplidos ahora",
                "missed_quip_upset_short": "no es un buen momento",
                "picked_quip": "¡qué lindo regalo!",
                "reload_quip": "¡bienvenido de vuelta!",
                "picked_game_name": "Pong",
                "story_begin_quip": "Había una vez...",
                "good_quip": "¡Ese es un buen nombre!",
                "limit_quip": "ya hemos hablado de eso",
                "love_quip": "yo también te amo muchísimo",
                "v_quip": "Vaya, parece que algo falló",
                "menuoption": "...No lo eres, ¿verdad?",
                "new_name_question": "¿Puedes decirme cuál es?",
                "same_name_question": "¿Ese mismo?",
                "question": "¿Qué opinas?",
                "holiday_str": "Navidad",
                "ntext": "J̸u̸s̸t̸ ̸M̸o̸n̸i̸k̸a̸",
                "line_end": "adorable amigo verde que tengo en mi escritorio no lo es.",
                "line_ending": " con todos en ella siendo solo un cascarón vacío.",
                "detected_ks_folder": "Katawa Shoujo",
                "pen_name": "Jugador",
                "tempinstrument": "piano",
                "tempmusicgenre": "pop",
                "x_side_eye": "izquierdo",
                "bday_msg_capped": "¡Feliz cumpleaños!",
                "_return": "1999",
                "player_nick": "cariño",
                "title_cased_hes": "Ella",
                "end_of_line": "parece que no puedo salir de este salón de clases",
                "the": "los"
            }
            
            var_lower = var_name.lower()
            for key, val in mock_fallbacks.items():
                if key in var_lower or var_lower in key.lower():
                    return val
                    
            # Fallback final: literal
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
                for _line in lines:
                    identifier = _line.strip()
                    if identifier and not identifier.startswith("#"):
                        ids.append(identifier)
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
                    
                # Define set of words to ignore when scanning inside bracket tags
                IGNORE_WORDS = {
                    "renpy", "store", "random", "choice", "substitute", "globals", "locals", 
                    "getattr", "hasattr", "setattr", "len", "str", "int", "float", "bool", 
                    "list", "dict", "set", "tuple", "eval", "exec", "import", "from", "as",
                    "if", "else", "elif", "not", "or", "and", "in", "is", "for", "while",
                    "True", "False", "None", "mas_a_an_str", "mas_getEV", "mas_isMoniUpset",
                    "mas_isMoniDis", "mas_isMoniHappy", "mas_isMoniNormal", "mas_isMoniBroken"
                }
                
                # Excluded pronoun/game variables to avoid resolving them
                EXCLUDED_VARS = {
                    "player", "m_name", "mas_get_playernickname", "p_nickname", "inputname",
                    "un_una", "el_la", "lo_la", "uno_una", "el_ella", "cap_el_ella", 
                    "al_ala", "del_dela", "hero", "buen_buena", "dormilon_dormilona", 
                    "or_ora", "on_ona", "amigo_amiga", "dor_dora", "tores", "e_a", "o_a"
                }

                # Find all brackets and extract candidate variables inside them
                tags = re.findall(r'\[([^\]]+)\]', what_str)
                vars_in_text = []
                # Ignorar librerías y palabras clave de python
                IGNORE_WORDS = ["renpy", "substitute", "store", "mas_utils", "datetime", "mas_calendar", "genFormalDispDate", "os", "path", "normpath", "isinstance", "len", "int", "str", "persistent", "beautiful", "enchanting", "if", "else"]
                for tag in tags:
                    # Ren'Py requires the variable to exist even if it has !t or !u
                    tag = tag.replace("!t", "").replace("!u", "")
                    # Match all word tokens inside the tag
                    words = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', tag)
                    for word in words:
                        if word not in IGNORE_WORDS and word not in EXCLUDED_VARS:
                            if word not in vars_in_text:
                                vars_in_text.append(word)
                                
                log_debug("Variables found in dialogue string: " + str(vars_in_text))
                placeholders = {}
                for var in vars_in_text:
                    if var == "line" and hasattr(renpy.store, "line"):
                        delattr(renpy.store, "line")
                    if not hasattr(renpy.store, var):
                        log_debug("Variable '" + var + "' is not present in renpy.store. Attempting resolution...")
                        
                        # Try to resolve the variable value safely
                        resolved_val = resolve_missing_variable_safely(filename, linenumber, var)
                        
                        if resolved_val is not None:
                            log_debug("  Successfully set '" + var + "' to: " + str(resolved_val))
                            setattr(renpy.store, var, resolved_val)
                        else:
                            # Fallback placeholder, use [[var]] to escape for renpy so it literally shows [var]
                            log_debug("  Resolution failed for '" + var + "'. Setting literal fallback placeholder.")
                            setattr(renpy.store, var, "[[" + var + "]]")
                        placeholders[var] = True
                    else:
                        log_debug("Variable '" + var + "' already exists in renpy.store with value: " + str(getattr(renpy.store, var)))
                        
                # Apply pose/expression attributes if defined
                if attributes:
                    renpy.game.context().say_attributes = attributes
                    
                # Capture the final substituted dialogue for the output log
                try:
                    sub_what, _ignored_1 = renpy.substitutions.substitute(what_str)
                    speaker_name = "Monika"
                    if hasattr(who_obj, "name"):
                        sub_who, _ignored_2 = renpy.substitutions.substitute(who_obj.name)
                        speaker_name = sub_who
                    elif who_str:
                        speaker_name = str(who_str)
                    
                    # Remove text tags like {b}, {w=0.5} to make the output clean
                    clean_what = re.sub(r'\{.*?\}', '', sub_what)
                    clean_what = clean_what.replace("[[", "[").replace("]]", "]")
                    dialogue_output_log.append("[" + identifier + "] " + speaker_name + ': "' + clean_what + '"')
                except Exception as e:
                    dialogue_output_log.append("[" + identifier + "] (Failed to capture text: " + str(e) + ")")
                    
                error_msg = None
                try:
                    renpy.say(who_obj, what_str, interact=interact)
                except Exception as ex:
                    error_msg = str(ex)
                finally:
                    # Restore context attributes and clean up temporary store placeholders
                    renpy.game.context().say_attributes = None
                    for var in placeholders:
                        if hasattr(renpy.store, var):
                            delattr(renpy.store, var)
                            
                if error_msg:
                    log_debug("Error displaying dialogue for hash " + identifier + ": " + error_msg)
                    dialogue_output_log.append("[" + identifier + "] (Failed during display: " + error_msg + ")")
                        
            elif isinstance(node, renpy.ast.Python):
                # DO NOT execute Python nodes during a dry-run test!
                # They can cause silent crashes or unexpected jumps by modifying game state or executing renpy.jump()/quit().
                log_debug("Skipping Python node to prevent engine crashes out of context.")
                dialogue_output_log.append("[" + identifier + "] (Python execution skipped for stability)")
            else:
                log_debug("Unsupported statement node: " + type(node).__name__)
                dialogue_output_log.append("[" + identifier + "] (Unsupported statement node type: " + type(node).__name__ + ")")
                
        # Write debug logs to file
        log_debug("=== TRANSLATION TESTER RUN FINISHED ===")
        try:
            with codecs.open(debug_filepath, "w", "utf-8") as f:
                for line in debug_log:
                    f.write(line + "\n")
            with codecs.open(output_filepath, "w", "utf-8") as f:
                for line in dialogue_output_log:
                    f.write(line + "\n")
        except Exception as e:
            renpy.say(m, "Error saving log files: " + str(e))
                
    m 1hua "Translation testing finished successfully."
    return
