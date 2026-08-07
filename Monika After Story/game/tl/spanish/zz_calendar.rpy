# TODO: Translation updated at 2026-03-31 15:02

# game/zz_calendar.rpy:2163
translate spanish _first_time_calendar_use_9c5ff161:

    # m 1eub "Oh, you want to take another look at that pretty calendar hanging on the wall, [player]?"
    m 1eub "Oh, ¿quieres echar otro vistazo a ese bonito calendario colgado en la pared, [player]?"

# game/zz_calendar.rpy:2164
translate spanish _first_time_calendar_use_6b069f8b:

    # m 3hua "It helps me keep track of important events, like your birthday, ehehe~"
    m 3hua "Me ayuda a estar atenta a eventos importantes, como tu cumpleaños, jeje~"

# game/zz_calendar.rpy:2166
translate spanish _first_time_calendar_use_72782367:

    # m 1eub "Oh, I see you noticed that pretty calendar hanging on the wall, [player]."
    m 1eub "Oh, veo que te has fijado en ese bonito calendario colgado en la pared, [player]."

# game/zz_calendar.rpy:2167
translate spanish _first_time_calendar_use_b262b5f6:

    # m 3hua "It helps me keep track of important events, ehehe~"
    m 3hua "Me ayuda a estar atenta a eventos importantes, jeje~"

# game/zz_calendar.rpy:2169
translate spanish _first_time_calendar_use_ce9b94b7:

    # m 1eua "Here, let me show you."
    m 1eua "Ven, deja que te lo enseñe."

# game/zz_calendar.rpy:2174
translate spanish _first_time_calendar_use_f7af61a6:

    # m 1hua "Pretty cool, right?"
    m 1hua "Está genial, ¿verdad?"

# game/zz_calendar.rpy:2175
translate spanish _first_time_calendar_use_d2dea50f:

    # m 3eua "Feel free to check the calendar whenever you want."
    m 3eua "Puedes revisar el calendario cuando quieras."

# game/zz_calendar.rpy:2176
translate spanish _first_time_calendar_use_46b69767:

    # m 1lksdla "Except for when I'm in the middle of talking, of course."
    m 1lksdla "A menos que esté hablando contigo en ese momento, claro."

translate spanish strings:

    # game/zz_calendar.rpy:221
    old "< Go back"
    new "< Volver"

    # game/zz_calendar.rpy:303
    old "Select a Date"
    new "Selecciona una fecha"

    # game/zz_calendar.rpy:311
    old "Calendar"
    new "Calendario"

    # game/zz_calendar.rpy:726
    old "Events for the day:"
    new "Eventos del día:"

    # game/zz_calendar.rpy:1883
    old "New Year's Day"
    new "Año Nuevo"

    # game/zz_calendar.rpy:1884
    old "Valentine's Day"
    new "Día de San Valentín"

    # game/zz_calendar.rpy:1886
    old "Day I Became an AI"
    new "Día en que me convertí en una IA"

    # game/zz_calendar.rpy:1887
    old "My Birthday"
    new "Mi Cumpleaños"

    # game/zz_calendar.rpy:1888
    old "Halloween"
    new "Halloween"

    # game/zz_calendar.rpy:1889
    old "Christmas Eve"
    new "Nochebuena"

    # game/zz_calendar.rpy:1890
    old "Christmas"
    new "Navidad"

    # game/zz_calendar.rpy:1891
    old "New Year's Eve"
    new "Nochevieja"

    # game/zz_calendar.rpy:1914
    old "Your Birthday"
    new "Tu Cumpleaños"

    # game/zz_calendar.rpy:1926
    old "Our First Kiss"
    new "Nuestro Primer Beso"

    # game/zz_calendar.rpy:1943
    old "Winter"
    new "Invierno"

    # game/zz_calendar.rpy:1944
    old "Spring"
    new "Primavera"

    # game/zz_calendar.rpy:1945
    old "Summer"
    new "Verano"

    # game/zz_calendar.rpy:1946
    old "Autumn"
    new "Otoño"

init 10 python in mas_calendar:

    SPANISH_MONTH_NAMES = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    import store
    if hasattr(store, "MASCalendar"):
        store.MASCalendar.MONTH_NAMES = ["Desconocido", "Enero", "Febrero",
            "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre",
            "Noviembre", "Diciembre"]
        store.MASCalendar.DAY_NAMES = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves",
            "Viernes", "Sábado"]

    def getZodiacSign(date):
        """
        Sobrescribe getZodiacSign con los nombres en español.
        """
        import bisect
        zodiac_signs = [
            (1, 19, "capricornio"), (2, 18, "acuario"), (3, 20, "piscis"), (4, 19, "aries"),
            (5, 20, "tauro"), (6 ,21, "géminis"), (7, 22, "cáncer"), (8, 22, "leo"),
            (9, 22, "virgo"), (10, 22, "libra"), (11, 22, "escorpio"), (12, 21, "sagitario"),
            (12, 31, "capricornio")
        ]
        index = bisect.bisect(zodiac_signs, (date.month, date.day))
        
        return zodiac_signs[index][-1]

    def _formatDay(day):
        """
        En español no solemos usar sufijos ordinales para las fechas.
        """
        return str(day)

    def _formatYears(years):
        """
        Traducción de relativos de años.
        """
        if years <= 0:
            return ""
        
        if years == 1:
            return "el año pasado"
        
        return "hace " + str(years) + " años"

    def genFriendlyDispDate_d(_date):
        """
        Genera una fecha amigable en formato español: D de M de Y.
        """
        import datetime
        disp_month = SPANISH_MONTH_NAMES[_date.month - 1]
        disp_day = str(_date.day)
        
        _today = datetime.date.today()
        _day_diff = _today - _date
        _year_diff = _today.year - _date.year
        
        _cout = list()
        
        if _today.month == _date.month and _today.day == _date.day:
            if _year_diff == 0:
                _cout = ["hoy"]
            else:
                _cout = [_formatYears(_year_diff), "en esta fecha"]
        
        elif _day_diff.days <= 365: 
            _cout = [disp_day, "de", disp_month]
        
        elif _year_diff <= 10:
            _cout = [_formatYears(_year_diff), "el", disp_day, "de", disp_month]
        
        else:
            _cout = [
                disp_day,
                "de",
                disp_month,
                "del",
                str(_date.year)
            ]
        
        return (" ".join(_cout), _day_diff)

    def genFormalDispDate(_date):
        """
        Genera la fecha formal requerida por el usuario: D de M del Y.
        """
        import datetime
        return (
            "{} de {} del {}".format(
                str(_date.day),
                SPANISH_MONTH_NAMES[_date.month - 1],
                str(_date.year)
            ),
            datetime.date.today() - _date
        )
