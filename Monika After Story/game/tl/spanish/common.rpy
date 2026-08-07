translate spanish strings:

    # _errorhandling.rpym:528
    old "Open"
    new "Abrir"

    # _errorhandling.rpym:530
    old "Opens the traceback.txt file in a text editor."
    new "Abre el archivo de rastreo 'traceback.txt' en un editor de texto."

    # _errorhandling.rpym:532
    old "Copy"
    new "Copiar"

    # _errorhandling.rpym:534
    old "Copies the traceback.txt file to the clipboard."
    new "Copia el archivo traceback.txt al portapapeles."

    # _errorhandling.rpym:542
    old "Copy BBCode"
    new "Copiar BBCode"

    # _errorhandling.rpym:544
    old "Copies the traceback.txt file to the clipboard as BBcode for forums like https://lemmasoft.renai.us/."
    new "Copia el archivo traceback.txt en el portapapeles como BBcode para foros como https://lemmasoft.renai.us/."

    # _errorhandling.rpym:546
    old "Copy Markdown"
    new "Copiar Markdown"

    # _errorhandling.rpym:548
    old "Copies the traceback.txt file to the clipboard as Markdown for Discord."
    new "Copia el archivo traceback.txt al portapapeles como Markdown para Discord."

    # _errorhandling.rpym:561
    old "An exception has occurred."
    new "Ha ocurrido una excepción."

    # _errorhandling.rpym:581
    old "Rollback"
    new "Volver atrás"

    # _errorhandling.rpym:583
    old "Attempts a roll back to a prior time, allowing you to save or choose a different choice."
    new "Intenta volver a un momento anterior y permite guardar o escoger una opción diferente."

    # _errorhandling.rpym:586
    old "Ignore"
    new "Ignorar"

    # _errorhandling.rpym:590
    old "Ignores the exception, allowing you to continue."
    new "Ignora la excepción y permite continuar."

    # _errorhandling.rpym:592
    old "Ignores the exception, allowing you to continue. This often leads to additional errors."
    new "Ignora la excepción y permite continuar. Suele conllevar más errores."

    # _errorhandling.rpym:596
    old "Reload"
    new "Recargar"

    # _errorhandling.rpym:598
    old "Reloads the game from disk, saving and restoring game state if possible."
    new "Recarga el juego desde el disco, guardando y restaurando la partida si es posible."

    # _errorhandling.rpym:601
    old "Console"
    new "Consola"

    # _errorhandling.rpym:603
    old "Opens a console to allow debugging the problem."
    new "Abre una consola y permite depurar el problema."

    # _errorhandling.rpym:613
    old "Quits the game."
    new "Sale del juego."

    # _errorhandling.rpym:637
    old "Parsing the script failed."
    new "Error en el análisis del código."

    # _errorhandling.rpym:663
    old "Opens the errors.txt file in a text editor."
    new "Abre el archivo de errores, 'errors.txt', en un editor de texto."

    # _errorhandling.rpym:667
    old "Copies the errors.txt file to the clipboard."
    new "Copia el archivo errors.txt al portapapeles."

    # _errorhandling.rpym:683
    old "Copies the errors.txt file to the clipboard as BBcode for forums like https://lemmasoft.renai.us/."
    new "Copia el archivo errors.txt en el portapapeles como BBcode para foros como https://lemmasoft.renai.us/."

    # _errorhandling.rpym:687
    old "Copies the errors.txt file to the clipboard as Markdown for Discord."
    new "Copia el archivo errors.txt al portapapeles como Markdown para Discord."

    # errorhandling.rpym text content
    # _errorhandling.rpym:697
    old "While running game code:"
    new "Durante la ejecución del código:"

    # _errorhandling.rpym:701
    old "Full traceback:"
    new "Rastreo completo:"


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

