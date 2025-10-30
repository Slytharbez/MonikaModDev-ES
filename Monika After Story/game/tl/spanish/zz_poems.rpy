# TODO: Translation updated at 2026-03-31 15:02

# game/zz_poems.rpy:344
translate spanish monika_showpoem_ccc4d9a5:

    # m 1rkc "Alright, [player]..."
    m 1rkc "De acuerdo, [player]..."

# game/zz_poems.rpy:348
translate spanish monika_showpoem_aec3fbc2:

    # m 3hua "Alright!"
    m 3hua "¡Muy bien!"

# game/zz_poems.rpy:353
translate spanish monika_showpoem_3aa9bd6c:

    # m 3eka "I hope you liked it, [player]."
    m 3eka "Espero que te haya gustado, [player]."

# game/zz_poems.rpy:355
translate spanish monika_showpoem_851a6cd5:

    # m 1eka "Would you like to read another poem?{nw}"
    m 1eka "¿Te gustaría leer otro poema?{nw}"

# game/zz_poems.rpy:358
translate spanish monika_showpoem_27e2b183:

    # m "Would you like to read another poem?{fast}" nointeract
    m "¿Te gustaría leer otro poema?{fast}" nointeract

# game/zz_poems.rpy:364
translate spanish monika_showpoem_bd219ce5:

    # m 1eua "Alright, [player]."
    m 1eua "De acuerdo, [player]."

translate spanish strings:

    # game/zz_poems.rpy:303
    old "Can I read one of your poems again?"
    new "¿Puedo volver a leer uno de tus poemas?"

    # game/zz_poems.rpy:330
    old "Which poem would you like to read?"
    new "¿Qué poema te gustaría leer?"


init 999 python:
    # Normalize line endings of all poems in memory to \n (LF)
    # This ensures they match perfectly with Ren'Py 6 translation catalog.
    for k, v in globals().items():
        if hasattr(v, 'title') and hasattr(v, 'text') and isinstance(v.text, (str, unicode)):
            v.text = v.text.replace("\r\n", "\n")
            if isinstance(v.title, (str, unicode)):
                v.title = v.title.replace("\r\n", "\n")
