# TODO: Translation updated at 2026-03-31 15:02

# game/event-handler.rpy:3663
translate spanish mas_bookmarks_unbookmark_c42f8f06:

    # m 1dsa "Okay, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    m 1dsa "Okey, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    
# game/event-handler.rpy:3664
translate spanish mas_bookmarks_unbookmark_73747bba:

    # m 3hua "All done!"
    m 3hua "¡Todo listo!"

translate spanish strings:

    # game/event-handler.rpy:3300
    old "I would like to see 'Unseen' ([unseen_num]) again"
    new "Quisiera ver los ([unseen_num]) diálogos 'Nuevos' otra vez."

    # game/event-handler.rpy:3321
    old "{b}Unseen{/b}"
    new "{b}Nuevo{/b}"

    # game/event-handler.rpy:3323
    old "Bookmarks"
    new "Marcadores"

    # game/event-handler.rpy:3324
    old "Hey, [m_name]..."
    new "Hey, [m_name]..."

    # game/event-handler.rpy:3326
    old "Repeat conversation"
    new "Repetir diálogos"

    # game/event-handler.rpy:3329
    old "I love you too!"
    new "¡Yo también te amo!"

    # game/event-handler.rpy:3331
    old "I love you!"
    new "¡Te amo!"

    # game/event-handler.rpy:3332
    old "I feel..."
    new "Me siento..."

    # game/event-handler.rpy:3333
    old "Goodbye"
    new "Adiós"

    # game/event-handler.rpy:3334
    old "Nevermind"
    new "No importa"

    # game/event-handler.rpy:3339
    old "Android Menu"
    new "Menú para Android"

    # game/event-handler.rpy:3393
    old "I don't want to see this menu anymore"
    new "No quiero ver más este menú."

    # game/event-handler.rpy:3608
    old "I'd like to remove a bookmark"
    new "Me gustaría eliminar un marcador."

    # game/event-handler.rpy:3676
    old "{0}{1}{2}"
    new "{0}{1}{2}"

    # game/event-handler.rpy:3700
    old "Which bookmarks do you want to remove?"
    new "¿Qué marcadores quieres eliminar?"

    # game/event-handler.rpy:3703
    old "Just select the bookmark if you're sure you want to remove it."
    new "Solo selecciona el marcador si estás segur[o_a] de que quieres eliminarlo."

    # game/event-handler.rpy:3705
    old "Remove selected"
    new "Eliminar seleccionados"

    # game/event-handler.rpy (multiple locations)
    old "Sure, [m_name]."
    new "Por supuesto, [m_name]."

    # game/event-handler.rpy (multiple locations)
    old "Yeah."
    new "Sí."

init 5 python:

    MAS_CAT_TRANS = {
        # game/script-topics.rpy and others - categories with _()
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
        Returns the translated category label for conversations.
        Only translates when the active language is 'spanish'.
        If no translation is available, returns the original category.
        """

        if _preferences.language == "spanish":

            return MAS_CAT_TRANS.get(cat, cat)
        return cat

