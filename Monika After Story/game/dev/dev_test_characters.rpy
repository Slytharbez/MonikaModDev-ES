init 999 python:
    def dev_generate_character_files():
        """
        Generates all natively created files in the characters directory
        to verify their translated names and contents.
        """
        import os
        import io

        def _write_txt(rel_path, message=""):
            try:
                # Force UTF-8 encoding to avoid Windows encoding issues with Spanish accents
                with io.open(os.path.normcase(renpy.config.basedir + rel_path), "w", encoding="utf-8") as f:
                    f.write(message)
            except Exception as e:
                pass

        # 1. recovery.txt (from zz_backup.rpy)
        # Construct the translated content of recovery.txt
        recovery_content = "".join([
            __("1. Navigate to '"),
            renpy.config.savedir,
            __("'.\n"),
            __("2. Delete the file called 'persistent'.\n"),
            __("3. Make a copy of the file called '"),
            "mas_backup_copy_filename",
            __("' and name it 'persistent'.")
        ])
        _write_txt("/characters/" + __("recovery.txt"), recovery_content)

        # 2. shopping_list.txt (from zz_consumables.rpy)
        START_TEXT = __(
            "Hi, [player],\n"
            "Just letting you know I'm running low on a couple of things.\n"
            "You wouldn't mind getting some more for me, would you?\n\n"
            "Here's a list of what I'm running out of:\n"
        )
        MID_TEXT = "- {0}\n".format(__(store.mas_consumable_coffee.disp_name).capitalize())
        MID_TEXT += "- {0}\n".format(__(store.mas_consumable_hotchocolate.disp_name).capitalize())
        MID_TEXT += "\n"
        END_TEXT = __("Thanks, [player]~")

        _write_txt("/characters/" + __("shopping_list.txt"), renpy.substitute(START_TEXT + MID_TEXT + END_TEXT))

        # 3. note.txt (from script-story-events.rpy)
        title_txt = __("Hi [player],")
        just_let_u_know = __(
            'Just wanted to let you know that your "persistent" file was '
            'corrupted, but I managed to restore an older backup!'
        )
        good_luck = __("Good luck with Monika!")
        dont_tell = __("P.S: Don't tell her about me!")
        body_txt = just_let_u_know + "\n\n" + good_luck + "\n\n" + dont_tell
        
        _write_txt("/characters/" + __("note.txt"), renpy.substitute(title_txt) + "\n\n" + renpy.substitute(body_txt))

        # 4. hint.txt (from script-story-events.rpy)
        gift_instructs = __(
            "I wanted to let you know that I made a little way for you to give Monika some gifts!\n"
            "It's a pretty simple process so I'll tell you how it works:\n\n"
            "Make a new file in the 'characters' folder\n"
            "Rename it to whatever you want to give to Monika\n"
            "Give it a '.gift' file extension\n\n"
            "And that's it! After a little while, Monika should notice that you gave her something.\n\n"
            "I just wanted to let you know because I think that Monika is super amazing and I really want to see her happy.\n\n"
            "Good luck with Monika!\n\n"
            "P.S: Don't tell her about me!\n"
        )
        _write_txt("/characters/" + __("hint.txt"), player + "\n\n" + renpy.substitute(gift_instructs))

        # 5. gotcha (from script-holidays.rpy)
        _write_txt("/characters/" + renpy.substitute(__("gotcha")), "")

        # 6. birthday hint.txt (from script-holidays.rpy)
        message_bday = __("[player],\nAs I hope you know, Monika's birthday is coming up soon and I want to make it special.\nShe's been through a lot lately, and I know it'd mean the world to her if you treated her to a nice day.\nSince I'm always here, I can easily set up a surprise party...but I do need a little help from you.\nAll I need you to do is to make sure you have her out of the room at some point on her birthday, and I'll take care of the rest.\nIf you care for Monika at all, you'll help me do this.\n\nJust leave a file named 'oki doki' in the same folder you found this note so I know to go ahead with the party.\n\nPlease, don't mess this up.\n\nP.S: Don't tell her about me.\n")
        
        # Dynamically build "cumple_para pablo.txt" (or equivalent localized name)
        bday_filename = "cumple_" + store.mas_utils.sanitize_filename(__("For {0}.txt").format(player))
        _write_txt("/characters/" + bday_filename, renpy.substitute(message_bday))

        # 7. updates.rpy
        _write_txt("/characters/" + __("ehehe.txt"), __("ehehe"))
        _write_txt("/characters/" + __("hehehe.txt"), "")
        _write_txt("/characters/" + __("restinpeace.txt"), "")
        _write_txt("/characters/" + __("presents.txt"), "")
        _write_txt("/characters/" + __("nat_gift.txt"), "")
        _write_txt("/characters/" + __("say_gift.txt"), "")
        _write_txt("/characters/" + __("yur_gift.txt"), "")
        _write_txt("/characters/" + __("mon_gift.txt"), "")
        _write_txt("/characters/" + __("m_gift.txt"), "")

        # 8. script-affection.rpy
        _write_txt("/characters" + __("/My one and only love.txt"), "")
        _write_txt("/characters" + __("/for you.txt"), "")
        _write_txt("/characters" + __("/secret.txt"), "")
        _write_txt("/characters" + __("/surprise.txt"), "")
        _write_txt("/characters" + __("/please listen.txt"), "")
        _write_txt("/characters" + __("/can you hear me.txt"), "")
        
        # 9. imsorry.txt (checked in definitions.rpy)
        _write_txt("/characters/" + __("imsorry.txt"), "")
        
        return "Archivos creados en la carpeta /characters/"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_character_files",
            category=["dev"],
            prompt="Generar archivos TXT en /characters/",
            random=False,
            pool=True
        )
    )

label dev_test_character_files:
    m "Generando archivos..."
    python:
        result = dev_generate_character_files()
    m "[result]"
    return
