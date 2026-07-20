init -1000 python:

    # Early traceback mirror translation function and registration
    import sys
    import collections
    # 1. Define the translation dictionaries early

    if not hasattr(store, '_log_tl'):

        store._log_tl = {}
    # Pre-populate Spanish log/traceback translations
    store._log_tl["spanish"] = {
        "I'm sorry, but an uncaught exception occurred.": "Lo sentimos, pero ha ocurrido una excepción no controlada.",
        "-- Full Traceback ------------------------------------------------------------": "-- Rastreo Completo ------------------------------------------------------------",
        "Full traceback:": "Rastreo Completo:",
        "While running game code:": "Mientras se ejecutaba el código del juego:",
        "While loading the script.": "Mientras se cargaba el script.",
        "Before loading the script.": "Antes de cargar el script.",
        "After loading the script.": "Después de cargar el script.",
        "While executing init code:": "Mientras se ejecutaba el código de inicialización:",
        "After initialization, but before game start.": "Después de la inicialización, pero antes de iniciar el juego.",
        ", line ": ", línea ",
        ", in ": ", en ",
        "  File \"": "  Archivo \"",
        "File \"": "Archivo \"",
        "Exception: ": "Excepción: ",
        "ScriptError: ": "Error en Script: ",
        "ParseError: ": "Error de Análisis: ",
        "TypeError: ": "Error de Tipo: ",
        "AttributeError: ": "Error de Atributo: ",
        "SyntaxError: ": "Error de Sintaxis: ",
        "FileNotFoundError: ": "Error de Archivo No Encontrado: ",
        "NameError: ": "Error de Nombre: ",
        "ValueError: ": "Error de Valor: ",
        "KeyError: ": "Error de Clave: "
    }

    if not hasattr(store, '_register_log_translations'):

        def _register_log_translations(lang, translations):

            if lang not in store._log_tl:

                store._log_tl[lang] = {}
            store._log_tl[lang].update(translations)

            try:

                import renpy.log

                if not hasattr(renpy.log, "translations"):

                    renpy.log.translations = {}

                if lang not in renpy.log.translations:

                    renpy.log.translations[lang] = {}
                renpy.log.translations[lang].update(translations)

            except Exception:

                pass
        store._register_log_translations = _register_log_translations

    if not hasattr(store, '_translate_mirror_text'):

        def _translate_mirror_text(text):

            if not isinstance(text, (str, unicode)):

                return text

            if not text:

                return text

            try:

                lang = getattr(getattr(renpy.game, 'preferences', None), 'language', None)

                if not lang:

                    config_lang = getattr(renpy.config, 'language', None)

                    if config_lang and "spanish" in str(config_lang):

                        lang = "spanish"

            except:

                lang = None
            # Filter out noisy internal Ren'Py timing lines (e.g. "Init at script-X.rpyc:33 took 0.46s.")
            filtered_lines = []

            for line in text.splitlines(True):

                stripped = line.lstrip()

                if stripped.startswith("Init at ") and " took " in stripped:

                    continue
                filtered_lines.append(line)
            text = "".join(filtered_lines)

            if lang and lang in store._log_tl:

                for old_str, new_str in store._log_tl[lang].items():

                    text = text.replace(old_str, new_str)

            if lang == "spanish":

                try:

                    import re
                    # Regex for ctime format: Tue Jun 23 21:10:08 2026
                    pattern = r'\b([A-Z][a-z]{2})\s+([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\d{4})\b'
                    days_es = {
                        "Mon": "Lun", "Tue": "Mar", "Wed": "Mié", "Thu": "Jue",
                        "Fri": "Vie", "Sat": "Sáb", "Sun": "Dom"
                    }
                    months_es = {
                        "Jan": "Ene", "Feb": "Feb", "Mar": "Mar", "Apr": "Abr",
                        "May": "May", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago",
                        "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dic"
                    }

                    def replace_date(match):

                        day_en, month_en, date_num, time_str, year_str = match.groups()
                        day_es = days_es.get(day_en, day_en)
                        month_es = months_es.get(month_en, month_en)
                        return "{} {} {} {} {}".format(day_es, month_es, date_num, time_str, year_str)
                    text = re.sub(pattern, replace_date, text)

                except Exception:

                    pass
            return text
        store._translate_mirror_text = _translate_mirror_text
        # Monkeypatch python's traceback module to automatically translate tracebacks

        try:

            import traceback

            if not hasattr(traceback, "_original_format_exception"):

                traceback._original_format_exception = traceback.format_exception

                def _spanish_format_exception(*args, **kwargs):

                    res = traceback._original_format_exception(*args, **kwargs)

                    if isinstance(res, list):

                        return [_translate_mirror_text(s) for s in res]
                    return _translate_mirror_text(res)
                traceback.format_exception = _spanish_format_exception

            if not hasattr(traceback, "_original_format_tb"):

                traceback._original_format_tb = traceback.format_tb

                def _spanish_format_tb(*args, **kwargs):

                    res = traceback._original_format_tb(*args, **kwargs)

                    if isinstance(res, list):

                        return [_translate_mirror_text(s) for s in res]
                    return _translate_mirror_text(res)
                traceback.format_tb = _spanish_format_tb

            if not hasattr(traceback, "_original_format_list"):

                traceback._original_format_list = traceback.format_list

                def _spanish_format_list(*args, **kwargs):

                    res = traceback._original_format_list(*args, **kwargs)

                    if isinstance(res, list):

                        return [_translate_mirror_text(s) for s in res]
                    return _translate_mirror_text(res)
                traceback.format_list = _spanish_format_list

            if not hasattr(traceback, "_original_format_exception_only"):

                traceback._original_format_exception_only = traceback.format_exception_only

                def _spanish_format_exception_only(*args, **kwargs):

                    res = traceback._original_format_exception_only(*args, **kwargs)

                    if isinstance(res, list):

                        return [_translate_mirror_text(s) for s in res]
                    return _translate_mirror_text(res)
                traceback.format_exception_only = _spanish_format_exception_only

        except Exception:

            pass
    # 2. Register Spanish translation strings dynamically by intercepting
    # renpy.translation.translate_string. This avoids adding duplicates to
    # the translation mappings which causes "A translation ... already exists"
    # exceptions when common.rpy is processed normally.

    try:

        early_translations = {
            "While running game code:": "Durante la ejecución del código:",
            "Full traceback:": "Rastreo completo:",
            "An exception has occurred.": "Ha ocurrido una excepción.",
            "Rollback": "Volver atrás",
            "Attempts a roll back to a prior time, allowing you to save or choose a different choice.": "Intenta volver a un momento anterior y permite guardar o escoger una opción diferente.",
            "Ignore": "Ignorar",
            "Ignores the exception, allowing you to continue.": "Ignora la excepción y permite continuar.",
            "Ignores the exception, allowing you to continue. This often leads to additional errors.": "Ignora la excepción y permite continuar. Suele conllevar más errores.",
            "Reload": "Recargar",
            "Reloads the game from disk, saving and restoring game state if possible.": "Recarga el juego desde el disco, guardando y restaurando la partida si es posible.",
            "Console": "Consola",
            "Opens a console to allow debugging the problem.": "Abre una consola y permite depurar el problema.",
            "Quit": "Salir",
            "Quits the game.": "Salir del juego.",
            "Open": "Abrir",
            "Opens the traceback.txt file in a text editor.": "Abre el archivo de rastreo 'traceback.txt' en un editor de texto.",
            "Copy": "Copiar",
            "Copies the traceback.txt file to the clipboard.": "Copia el archivo traceback.txt al portapapeles.",
            "Copy BBCode": "Copiar BBCode",
            "Copies the traceback.txt file to the clipboard as BBcode for forums like https://lemmasoft.renai.us/.": "Copia el archivo traceback.txt en el portapapeles como BBcode para foros como https://lemmasoft.renai.us/.",
            "Copy Markdown": "Copiar Markdown",
            "Copies the traceback.txt file to the clipboard as Markdown for Discord.": "Copia el archivo traceback.txt al portapapeles como Markdown para Discord.",
            "Parsing the script failed.": "Error en el análisis del código.",
            "Opens the errors.txt file in a text editor.": "Abre el archivo de errores 'errors.txt' en un editor de texto.",
            "Copies the errors.txt file to the clipboard.": "Copia el archivo errors.txt al portapapeles.",
            "Copies the errors.txt file to the clipboard as BBcode for forums like https://lemmasoft.renai.us/.": "Copia el archivo errors.txt en el portapapeles como BBcode para foros como https://lemmasoft.renai.us/.",
            "Copies the errors.txt file to the clipboard as Markdown for Discord.": "Copia el archivo errors.txt al portapapeles como Markdown para Discord."
        }

        if not hasattr(store, '_original_translate_string'):

            store._original_translate_string = renpy.translation.translate_string

            def _early_translate_string(s, language=renpy.translation.Default):

                try:

                    if not isinstance(s, (str, unicode)):

                        s = unicode(s)

                except NameError:

                    if not isinstance(s, str):

                        s = str(s)

                if language is renpy.translation.Default:

                    language = getattr(getattr(renpy.game, 'preferences', None), 'language', None)

                if language == "spanish" and s in early_translations:

                    return early_translations[s]
                return store._original_translate_string(s, language)
            renpy.translation.translate_string = _early_translate_string

    except Exception as e:

        pass

default o_a = "o"
default un_una = "un"
default el_la = "el"
default lo_la = "lo"
default e_a = "e"
default uno_una = "uno"
default el_ella = "él"
default cap_el_ella = "Él"
default al_ala = "al"
default del_dela = "del"
default dormilon_dormilona = "dormilón"

init 1 python:

    _pronoun_map = getattr(store, "MAS_PRONOUN_GENDER_MAP", None)

    if _pronoun_map is not None:

        _pronoun_map.update({
            "o_a": {"M": "o", "F": "a", "X": "e"},    # Ej: list[o_a] -> listo / lista / liste
            "un_una": {"M": "un", "F": "una", "X": "un"}, # Ej: [un_una] chico -> un / una / un
            "el_la": {"M": "el", "F": "la", "X": "le"},   # Ej: [el_la] mejor -> el / la / le
            "lo_la": {"M": "lo", "F": "la", "X": "le"},   # Ej: [lo_la] veo -> lo / la / le
            "e_a": {"M": "e", "F": "a", "X": "e"},     # Ej: est[e_a] -> este / esta / este
            "uno_una": {"M": "uno", "F": "una", "X": "une"}, # Ej: [uno_una] -> uno / una / une
            "el_ella": {"M": "él", "F": "ella", "X": "elle"},
            "cap_el_ella": {"M": "Él", "F": "Ella", "X": "Elle"},
            "al_ala": {"M": "al", "F": "a la", "X": "al"},  # Ej: [al_ala] otro -> al / a la / al
            "del_dela": {"M": "del", "F": "de la", "X": "del"}, # Ej: [del_dela] otro -> del / de la / del
            "hero": {"M": "héroe", "F": "heroína", "X": "héroe"},  # Ej: mi [hero] -> mi héroe / mi heroína
            "buen_buena": {"M": "buen", "F": "buena", "X": "buene"},  # Ej: [buen_buena] chic[o_a] -> buen chico / buena chica
            "dormilon_dormilona": {"M": "dormilón", "F": "dormilona", "X": "dormilón"},
            "or_ora": {"M": "or", "F": "ora", "X": "ore"}, # Ej: jugad[or_ora] -> jugador / jugadora / jugadore
            "on_ona": {"M": "ón", "F": "ona", "X": "one"}, # Ej: campe[on_ona] -> campeón / campeona / campeone
            "amigo_amiga": {"M": "amigo", "F": "amiga", "X": "amigue"},
            "dor_dora": {"M": "dor", "F": "dora", "X": "dore"},
            "tores": {"M": "tores", "F": "toras", "X": "tores"},
        })

init 10 python:

    # Registrar alias 'decknou' para la baraja de NOU en español
    import store.mas_filereacts as mas_filereacts

    if hasattr(mas_filereacts, "filereact_map") and "noudeck" in mas_filereacts.filereact_map:

        mas_filereacts.filereact_map["decknou"] = mas_filereacts.filereact_map["noudeck"]

# Fix for nickname prompt language mismatch

init 999 python:

    if "monika_affection_nickname" in persistent.event_database:

        ev = store.mas_getEV("monika_affection_nickname")

        if ev:

            # Temporarily unlock the prompt to allow updates
            Event.unlockInit("prompt", ev=ev)
            # Re-evaluate the prompt with the translation function _()
            ev.prompt = _("Can I call you a different nickname?")
            # Lock it back to preserve MAS standards
            Event.lockInit("prompt", ev=ev)

# =============================================================================
# DICCIONARIO EXPLÍCITO DE CATEGORÍAS DE CONVERSACIÓN
# Se usa en event-handler.rpy para traducir las categorías del menú "Hablar".
# Más fiable que _() para strings dinámicos en Python blocks de Ren'Py.
# =============================================================================

init 5 python:

    MAS_CAT_TRANS = {
        # game/script-topics.rpy y otros - categorías con _()
        "advice":           "consejos",
        "affection":        "afecto",
        "anniversary":      "aniversario",
        "apology":          "disculpa",
        "appearance":       "apariencia",
        "art":              "arte",
        "be right back":    "ya regreso",
        "clothes":          "ropa",
        "club members":     "integrantes del club",
        "compliment":       "cumplidos",
        "creepy":           "espeluznante",
        "ddlc":             "ddlc",
        "development":      "desarrollo",
        "farewell":         "despedida",
        "fashion":          "moda",
        "food":             "comida",
        "funny":            "divertido",
        "games":            "juegos",
        "grammar tips":     "consejos de gramática",
        "holidays":         "festividades",
        "life":             "vida",
        "literature":       "literatura",
        "literature club":  "club de literatura",
        "location":         "ubicación",
        "media":            "multimedia",
        "misc":             "otros",
        "mod":              "mod",
        "monika":           "monika",
        "music":            "música",
        "nature":           "naturaleza",
        "philosophy":       "filosofía",
        "psychology":       "psicología",
        "python tips":      "consejos de Python",
        "romance":          "romance",
        "school":           "escuela",
        "science":          "ciencia",
        "society":          "sociedad",
        "song":             "canción",
        "sports":           "deportes",
        "spring":           "primavera",
        "story":            "historia",
        "summer":           "verano",
        "supplies":         "suministros",
        "technology":       "tecnología",
        "trivia":           "curiosidades",
        "us":               "nosotr[o_a]s",
        "weather":          "clima",
        "winter":           "invierno",
        "writing":          "escritura",
        "writing tips":     "consejos de escritura",
        "you":              "tú"
    }

    def mas_get_cat_label(cat):

        """
        Retorna la etiqueta traducida de una categoría de conversación.
        Solo traduce cuando el idioma activo es 'spanish'.
        Si no hay traducción disponible, retorna la categoría original.
        """

        if _preferences.language == "spanish":

            return MAS_CAT_TRANS.get(cat, cat)
        return cat

    def mas_nou_masc_color():

        """
        Retorna el color masculino traducido en español para los diálogos de NOU.
        Por ejemplo, 'red' -> 'rojo' y 'yellow' -> 'amarillo'.
        """

        try:

            color = store.mas_nou.game.monika.chosen_color

        except AttributeError:

            color = None

        if not color:

            return ""

        if _preferences.language == "spanish":

            return {
                "red": "rojo",
                "blue": "azul",
                "green": "verde",
                "yellow": "amarillo"
            }.get(color, color)
        return color

    def mas_translate_eye_color(color):

        """
        Traduce el color de ojos del jugador al español cuando el idioma activo es 'spanish'.
        Soporta colores estándar y heterocromía (tupla).
        """

        if not color:

            return ""

        if isinstance(color, tuple):

            translated_components = [mas_translate_eye_color(c) for c in color]

            if len(translated_components) == 2:

                return " y ".join(translated_components)
            return ", ".join(translated_components)

        if _preferences.language == "spanish":

            color_lower = color.lower()
            translations = {
                "blue": "azules",
                "brown": "marrones",
                "green": "verdes",
                "hazel": "avellana",
                "gray": "grises",
                "black": "negros",
                "mesmerizing": "fascinantes",
                "beautiful": "hermosos",
                "enchanting": "encantadores",
                "red": "rojos",
                "purple": "morados",
                "violet": "violetas",
                "amber": "ámbar",
                "yellow": "amarillos"
            }
            return translations.get(color_lower, color)
        return color

translate spanish strings:

    # game/screens.rpy:718
    old "Save"
    new "Guardar"
    
    # game/screens.rpy:2289
    old "No"
    new "No"

    # game/screens.rpy:2372
    old "Cancel"
    new "Cancelar"

    # game/screens.rpy:2398
    old "No."
    new "No."

    # game/chess.rpy:3274
    old "Done"
    new "Listo"

    # game/event-handler.rpy:3334
    old "Nevermind"
    new "No importa"

    # =========================================================================
    # OPCIONES DE MENÚ Y DIÁLOGOS GLOBALES / DUPLICADOS
    # =========================================================================

    # game/event-handler.rpy (multiple locations)
    old "Sure, [m_name]."
    new "Por supuesto, [m_name]."

    # game/event-handler.rpy (multiple locations)
    old "Yeah."
    new "Sí."

    # game/screens.rpy (multiple locations)
    old "Okay"
    new "Okey"

    # game/screens.rpy (multiple locations)
    old "Okay."
    new "Okey."

    # game/screens.rpy (multiple locations)
    old "Yes"
    new "Sí"

    # game/screens.rpy (multiple locations)
    old "Yes."
    new "Sí."

    # game/script-holidays.rpy (multiple locations)
    old "holiday"
    new "un día festivo"

init 999 python:

    # Dynamic hint translation formatter
    import store.mas_hangman as mas_hmg

    class SpanishHintFormatter(str):

        def format(self, *args, **kwargs):

            if _preferences.language == "spanish":

                author = args[0]

                if author == "I":

                    return "A mí me gustaría más esta palabra."
                translated_author = renpy.translation.translate_string(author)
                return "A {0} le gustaría más esta palabra.".format(translated_author)
            return str.format(self, *args, **kwargs)
    mas_hmg.HM_HINT = SpanishHintFormatter(mas_hmg.HM_HINT)
    # Save original builders
    _orig_buildEasyList = mas_hmg.buildEasyList
    _orig_buildNormalList = mas_hmg.buildNormalList
    _orig_buildHardList = mas_hmg.buildHardList

    def _strip_spanish_accents(s):

        mapping = {
            u'á': u'a', u'é': u'e', u'í': u'i', u'ó': u'o', u'ú': u'u',
            u'ü': u'u', u'ñ': u'n'
        }
        res = []

        for c in s:

            res.append(mapping.get(c, c))
        return "".join(res)

    def _patched_build_all_lists():

        # 1. Reload store.full_wordlist in Spanish using renpy.file to resolve tl/spanish/poemwords.txt
        store.full_wordlist = []

        with renpy.file('poemwords.txt') as wordfile:

            for line in wordfile:

                if not isinstance(line, str):

                    line = line.decode('utf-8')
                line = line.strip()

                if line == '' or line[0] == '#': continue

                x = line.split(',')
                store.full_wordlist.append(store.PoemWord(x[0], float(x[1]), float(x[2]), float(x[3])))
        # Clear the target all_hm_words lists
        mas_hmg.all_hm_words[mas_hmg.EASY_MODE][:] = []
        mas_hmg.all_hm_words[mas_hmg.NORM_MODE][:] = []
        mas_hmg.all_hm_words[mas_hmg.HARD_MODE][:] = []
        # 2. Add non-Monika words from full_wordlist to EASY_MODE (stripping accents)

        for word in store.full_wordlist:

            hm_tuple = store.MASPoemWord._build(word, 0)._hangman()
            w_str = _strip_spanish_accents(hm_tuple[0])
            mas_hmg.all_hm_words[mas_hmg.EASY_MODE].append((w_str, hm_tuple[1]))
        # 3. Translate and add Monika words to EASY_MODE (stripping accents)

        for m_word in mas_hmg.MONI_WORDS:

            translated_word = renpy.translation.translate_string(m_word)
            translated_word = _strip_spanish_accents(translated_word)
            hm_tuple = (translated_word, "I")
            mas_hmg.all_hm_words[mas_hmg.EASY_MODE].append(hm_tuple)
        # 4. Load NORM_MODE words from tl/spanish/MASpoemwords.txt (stripping accents)
        norm_wordlist = store.MASPoemWordList('tl/spanish/MASpoemwords.txt').wordlist

        for word in norm_wordlist:

            hm_tuple = word._hangman()
            w_str = _strip_spanish_accents(hm_tuple[0])
            mas_hmg.all_hm_words[mas_hmg.NORM_MODE].append((w_str, hm_tuple[1]))
        # 5. Load HARD_MODE words from tl/spanish/1000poemwords.txt (stripping accents)
        hard_wordlist = store.MASPoemWordList('tl/spanish/1000poemwords.txt').wordlist

        for word in hard_wordlist:

            hm_tuple = word._hangman()
            w_str = _strip_spanish_accents(hm_tuple[0])
            mas_hmg.all_hm_words[mas_hmg.HARD_MODE].append((w_str, hm_tuple[1]))
        # 6. Copy lists
        mas_hmg.copyWordsList(mas_hmg.EASY_MODE)
        mas_hmg.copyWordsList(mas_hmg.NORM_MODE)
        mas_hmg.copyWordsList(mas_hmg.HARD_MODE)

    def _rebuild_words_for_current_language():

        if _preferences.language == "spanish":

            _patched_build_all_lists()

        else:

            # Rebuild English lists to support dynamic language switching back to English
            # 1. Reload store.full_wordlist in English
            store.full_wordlist = []

            with renpy.file('poemwords.txt') as wordfile:

                for line in wordfile:

                    if not isinstance(line, str):

                        line = line.decode('utf-8')
                    line = line.strip()

                    if line == '' or line[0] == '#': continue

                    x = line.split(',')
                    store.full_wordlist.append(store.PoemWord(x[0], float(x[1]), float(x[2]), float(x[3])))
            # 2. Call original builders
            _orig_buildEasyList()
            _orig_buildNormalList()
            _orig_buildHardList()

    def _patched_buildEasyList():

        _rebuild_words_for_current_language()

    def _patched_buildNormalList():

        _rebuild_words_for_current_language()

    def _patched_buildHardList():

        _rebuild_words_for_current_language()
    mas_hmg.buildEasyList = _patched_buildEasyList
    mas_hmg.buildNormalList = _patched_buildNormalList
    mas_hmg.buildHardList = _patched_buildHardList
    # Monkey-patch addPlayername to dynamically reload words in the active language at runtime when starting hangman
    _orig_addPlayername = mas_hmg.addPlayername

    def _patched_addPlayername(mode):

        _rebuild_words_for_current_language()
        _orig_addPlayername(mode)
    mas_hmg.addPlayername = _patched_addPlayername
    # NOTA: Comentado para evitar corromper el persistent con clases personalizadas de la traducción.
    # El saludo dinámico se traduce dinámicamente en script-topics.rpy mediante [mas_globals_time_of_day_3state_es].
    # _good_tod_ev = store.mas_getEV("monika_good_tod")
    # if _good_tod_ev is not None:
    #     try:
    #         Event.unlockInit("prompt", ev=_good_tod_ev)
    #         _good_tod_ev.prompt = DynamicGreeting()
    #         Event.lockInit("prompt", ev=_good_tod_ev)
    #     except Exception:
    #         pass
    # Registramos mas_get_greeting en store para que [mas_get_greeting!t] funcione en los diálogos y menús.
    store.mas_globals_time_of_day_3state_es = DynamicGreeting()
    # If already initialized at startup under Spanish:

    if _preferences.language == "spanish":

        renpy.license = "Este programa contiene software libre bajo varias licencias, incluyendo la Licencia Pública General Reducida de GNU. Una lista completa de software está disponible en https://www.renpy.org/license.html."
        _patched_build_all_lists()
    # Guardar las quips originales en inglés para el soporte de cambio dinámico
    _orig_win_notif_quips = list(store.mas_win_notif_quips)
    _orig_other_notif_quips = list(store.mas_other_notif_quips)

    def _mas_spanish_language_callback(new_lang=None):
        _rebuild_words_for_current_language()
        # Traducir quips de notificaciones según el idioma
        if _preferences.language == "spanish":
            store.mas_win_notif_quips = [
                "[player], quiero hablar contigo de algo.",
                "[player], ¿estás ahí?",
                "¿Puedes venir un segundo?",
                "[player], ¿tienes un segundo?",
                "¡Tengo algo que decirte, [player]!",
                "¿Tienes un minuto, [player]?",
                "¡Tengo algo de qué hablar, [player]!"
            ]
            store.mas_other_notif_quips = [
                "¡Tengo algo de qué hablar, [player]!",
                "¡Tengo algo que decirte, [player]!",
                "Hey [player], quiero decirte algo.",
                "¿Tienes un minuto, [player]?"
            ]
        else:
            store.mas_win_notif_quips = list(_orig_win_notif_quips)
            store.mas_other_notif_quips = list(_orig_other_notif_quips)
    # Registrar el callback para cambios de idioma dinámicos
    if hasattr(config, "change_language_callbacks"):
        config.change_language_callbacks.append(_mas_spanish_language_callback)
    # Aplicarlo al inicio del juego según la preferencia actual
    try:
        _mas_spanish_language_callback(renpy.game.preferences.language)
    except Exception:
        pass

# =============================================================================
# SALUDO SEGÚN LA HORA DEL DÍA
# En inglés: "Good morning / afternoon / evening" → En español necesita formas
# distintas: "Buenos días", "Buenas tardes", "Buenas noches"
# Se sobreescribe el prompt del evento monika_good_tod de forma dinámica.
# =============================================================================

python early:

    # Python compatibility for basestring

    try:

        basestring

    except NameError:

        basestring = str

    def mas_es_get_greeting():
        """Devuelve el saludo completo en español según la hora del día."""
        tod = getattr(store.mas_globals, "time_of_day_4state", None) if hasattr(store, "mas_globals") else None
        if tod == "morning":
            return "Buenos días"
        elif tod in ("afternoon", "evening"):
            return "Buenas tardes"
        else:
            return "Buenas noches"

    class DynamicGreeting(object):
        def __str__(self):
            return mas_es_get_greeting()
        def __unicode__(self):
            return unicode(mas_es_get_greeting())
        def __repr__(self):
            return repr(mas_es_get_greeting())
        def decode(self, *args, **kwargs):
            return mas_es_get_greeting().decode(*args, **kwargs)
        def replace(self, *args, **kwargs):
            return mas_es_get_greeting().replace(*args, **kwargs)
        def lower(self):
            return mas_es_get_greeting().lower()
        def upper(self):
            return mas_es_get_greeting().upper()
        def startswith(self, prefix, *args):
            return mas_es_get_greeting().startswith(prefix, *args)
        def endswith(self, suffix, *args):
            return mas_es_get_greeting().endswith(suffix, *args)
        def find(self, sub, *args):
            return mas_es_get_greeting().find(sub, *args)
        def __len__(self):
            return len(mas_es_get_greeting())
        def __contains__(self, item):
            return item in mas_es_get_greeting()

    try:

        import store.mas_logging as mas_logging

    except Exception:

        mas_logging = None
    import logging
    # We want to translate date strings in log headers, build info, and log messages
    log_strings_translations = {
        "LOAD": "CARGAR",
        "Loading from backup": "Cargando desde copia de seguridad",
        "DATA HAS BEEN RESET": "LOS DATOS HAN SIDO REINICIADOS",
        "Loading from system": "Cargando desde el sistema",
        "LOAD?": "¿CARGAR?",
        "MISMATCHES": "DISCREPANCIAS",
        "LOAD COMPLETE": "CARGA COMPLETA",
        "SAVE": "GUARDAR",
        "SET BACKUP": "CREAR COPIA DE SEGURIDAD",
        "FAILED TO BACKUP, CURRENT DATA IS BAD": "FALLO AL CREAR COPIA DE SEGURIDAD, LOS DATOS ACTUALES NO SON VÁLIDOS",
        "!FREEZE!": "¡CONGELADO!",
        "!BYPASS!": "¡IGNORAR!",
        "capped loss": "pérdida limitada",
        "10 year diff": "diferencia de 10 años",
        "she missed you": "te extrañó",
        "VERSION:": "VERSIÓN:",
        " - build: ": " - compilación: ",
        "build:": "compilación:",
        "!ERROR! T_T": "¡ERROR! T_T",
        "persistent was corrupted! : ": "¡El archivo persistent estaba dañado! : ",
        " was corrupted: ": " estaba dañado: ",
        "no working backups found": "no se encontraron copias de seguridad funcionales",
        "working backup found: ": "copia de seguridad funcional encontrada: ",
        "no backups available": "no hay copias de seguridad disponibles",
        "Failed to rename existing persistent: ": "Fallo al renombrar el persistent existente: ",
        "Failed to copy backup persistent: ": "Fallo al copiar la copia de seguridad del persistent: ",
        "Failed to copy persistent to special: ": "Fallo al copiar el persistent al archivo especial: ",
        "Permission denied": "Permiso denegado",
        "Access is denied": "Acceso denegado",
        "No such file or directory": "No existe el archivo o directorio",
        "Attempting to load ": "Intentando cargar ",
        " loaded successfully.": " cargado correctamente.",
        " loaded successfully!": " cargado con éxito!",
        "Loading PNM ": "Cargando PNM ",
        "Failed to load file at ": "Error al cargar el archivo en ",
        "Failed to load json at ": "Fallo al cargar el archivo json en ",
        "Load failed.": "Error al cargar.",
        "load failed.": "error al cargar.",
        "verifying hair maps...": "verificando mapas de cabello...",
        "hair map verification complete!": "¡verificación de mapas de cabello completada!",
        "creating reactions for gifts...": "creando reacciones para regalos...",
        "gift reactions created successfully!": "¡reacciones de regalos creadas con éxito!",
        "reading JSON at ": "leyendo JSON en ",
        "loading ": "cargando ",
        " sprite object ": " objeto sprite ",
        " loaded successfully!": " cargado con éxito!",
        " loaded successfully! DRY RUN": " cargado con éxito! PRUEBA EN SECO",
        "Pose Map ": "Mapa de poses ",
        "Filter object ": "Objeto de filtro ",
        "Highlight object ": "Objeto de resaltado ",
        "Highlight Split object ": "Objeto de división de resaltado ",
        "Highlight object for key ": "Objeto de resaltado para la clave ",
        "mapping loaded successfully!": "¡mapeo cargado con éxito!",
        "Pose Arms ": "Brazos de pose ",
        "Arm ": "Brazo ",
        "hair_map loaded successfully!": "¡hair_map cargado con éxito!",
        "ex_props loaded successfully!": "¡ex_props cargados con éxito!",
        "sel_info loaded successfully!": "sel_info cargado con éxito!",
        "outfit mode data loaded successfully!": "¡datos de modo de atuendo cargados con éxito!",
        "INSTALLED SUBMODS:": "SUBMODS INSTALADOS:",
        "Background Object: ": "Objeto Background: ",
        "\nFilter System:\n\n": "\nSistema de filtros:\n\n",
        "\n\nRaw Filter Manager Data:\n": "\n\nDatos brutos del gestor de filtros:\n"
    }
    # Helper function to translate dates

    def _translate_log_date(text):

        import re
        days_es = {"Mon": "Lun", "Tue": "Mar", "Wed": "Mie", "Thu": "Jue", "Fri": "Vie", "Sat": "Sab", "Sun": "Dom"}
        months_es = {"Jan": "Ene", "Feb": "Feb", "Mar": "Mar", "Apr": "Abr", "May": "May", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago", "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dic"}
        date_pattern = r'\b([A-Z][a-z]{2})\s+([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\d{4})\b'

        def replace_date(match):

            day_en, month_en, date_num, time_str, year_str = match.groups()
            day_es = days_es.get(day_en, day_en)
            month_es = months_es.get(month_en, month_en)
            return "{} {} {} {} {}".format(day_es, month_es, date_num, time_str, year_str)
        return re.sub(date_pattern, replace_date, text)
    # Translate retroactively whatever was already written in mas_log.log during the very early boot

    try:

        import os
        log_dir = os.path.join(renpy.config.basedir, "log")
        mas_log_file = os.path.join(log_dir, "mas_log.log")

        if os.path.exists(mas_log_file):

            with open(mas_log_file, "r") as f:

                content = f.read()
            translated_content = _translate_log_date(content)

            for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                translated_content = translated_content.replace(eng, log_strings_translations[eng])

            if translated_content != content:

                with open(mas_log_file, "w") as f:

                    f.write(translated_content)

    except Exception:

        pass
    # Interceptar logging.Logger.makeRecord (traduce los mensajes base y los headers tempranos al crearse el LogRecord)

    if not hasattr(logging.Logger, "_original_makeRecord"):

        logging.Logger._original_makeRecord = logging.Logger.makeRecord

        def _spanish_makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):

            if isinstance(msg, basestring):

                msg = _translate_log_date(msg)
                # Ordenar por longitud de mayor a menor para evitar colisiones de subcadenas

                for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                    msg = msg.replace(eng, log_strings_translations[eng])
            return logging.Logger._original_makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra)
        logging.Logger.makeRecord = _spanish_makeRecord
    # Interceptar logging.Formatter para logs estandar (incluyendo aff_log y fallback)

    if not hasattr(logging.Formatter, "_original_format"):

        logging.Formatter._original_format = logging.Formatter.format

        def _spanish_format_base(self, record):

            if isinstance(record.msg, basestring):

                record.msg = _translate_log_date(record.msg)

                for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                    record.msg = record.msg.replace(eng, log_strings_translations[eng])
            formatted = logging.Formatter._original_format(self, record)
            formatted = _translate_log_date(formatted)

            for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                formatted = formatted.replace(eng, log_strings_translations[eng])
            return formatted
        logging.Formatter.format = _spanish_format_base
    # Interceptar MASLogFormatter especifico (por si acaso no delega)

    if mas_logging and hasattr(mas_logging, "MASLogFormatter") and not hasattr(mas_logging.MASLogFormatter, "_original_format"):

        mas_logging.MASLogFormatter._original_format = mas_logging.MASLogFormatter.format

        def _spanish_format_mas(self, record):

            if isinstance(record.msg, basestring):

                record.msg = _translate_log_date(record.msg)

                for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                    record.msg = record.msg.replace(eng, log_strings_translations[eng])
            formatted = mas_logging.MASLogFormatter._original_format(self, record)
            formatted = _translate_log_date(formatted)

            for eng in sorted(log_strings_translations.keys(), key=len, reverse=True):

                formatted = formatted.replace(eng, log_strings_translations[eng])
            return formatted
        mas_logging.MASLogFormatter.format = _spanish_format_mas

init 999 python:
    # Normalizar los finales de línea de todos los poemas en memoria a \n (LF)
    # Esto asegura que coincidan perfectamente con el catálogo de traducción de Ren'Py 6.
    for k, v in globals().items():
        if hasattr(v, 'title') and hasattr(v, 'text') and isinstance(v.text, (str, unicode)):
            v.text = v.text.replace("\r\n", "\n")
            if isinstance(v.title, (str, unicode)):
                v.title = v.title.replace("\r\n", "\n")
