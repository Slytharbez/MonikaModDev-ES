# Pronouns and Spanish Genders Map
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
default hero = "héroe"
default buen_buena = "buen"
default dormilon_dormilona = "dormilón"
default or_ora = "or"
default on_ona = "ón"
default amigo_amiga = "amigo"
default dor_dora = "dor"
default tores = "tores"

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


# Spanish Python Logger Patch
python early:

    # Python compatibility for basestring
    try:

        basestring

    except NameError:

        basestring = str

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
