# Generated from exact original presentation sections; Russian only.
# Standard choice panels reserve three Say lines and a whole long choice.
# History, thresholds, source flags, preferences and actions are unchanged.

init 905 python:
    def _ru_choice_reserve_tall():
        """Read native presentation only; never alter story/layout machine flags."""
        if not ru_is_active() or getattr(renpy.store, "choice_witch_override", False) or getattr(renpy.context(), "_menu", False):
            return False
        say = renpy.get_screen("say")
        if say is None or getattr(say, "hiding", False) or "what" in getattr(say, "hidden_widgets", {}):
            return False
        if renpy.get_screen("choice") is None:
            # Exact accepted narrator Say: reserve the native tall presentation.
            # No story flags, text, fonts or ordinary choice behavior are changed.
            scope = getattr(say, "scope", {})
            if scope.get("who") is not None or scope.get("what") != '{i}Кажется, его пасть поглощает всё ваше лицо. Зубы смыкаются вокруг вашей челюсти; тёплая влажность его рта почти душит вас, когда длинный раздвоенный язык выскальзывает наружу и скользит по вашей щеке изнутри, исследуя вас, словно живёт своей жизнью. Острые кончики его пальцев впиваются в кожу вашей головы, и вы чувствуете, как что-то цепкое, тонкое и странное — его хвост — обвивает ваши ноги, притягивая вас ещё ближе.{/i}':
                return False
        for overlay in ("history", "journal", "save", "load", "preferences"):
            if renpy.get_screen(overlay) is not None:
                return False
        props = renpy.get_displayable_properties("window", screen="say")
        if "background" in props:
            return False
        native_style = props.get("style", "window")
        if native_style in ("window", "window_character", "say_window"):
            return True
        # Native rollback/variant properties may carry an actual Style object.
        name = getattr(native_style, "name", ())
        return bool(name and name[0] in ("window", "window_character", "say_window"))

screen say(who, what):
    variant "ru_pilot"
    #if textbox_big:
    #    style_prefix "big_say"
    #else:
    #    style_prefix "say"
    style_prefix "say"
    window:

        id "window"

        if who is not None:

            window:
                id "namebox"
                if textbox_big or _ru_choice_reserve_tall():
                    style "big_namebox"
                else:
                    style "namebox"
                text who id "who"

        if textbox_big or _ru_choice_reserve_tall():
            text what id "what" ypos -95
        else:
            text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
    if new_quick_menu:
        use quick_menu



translate russian style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    #if renpy.get_screen("choice"):
    background ConditionSwitch("(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == True and persistent.textbox_contrast == True", Image("gui/high_contrast_textbox_decision_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == False and persistent.textbox_contrast == True", Image("gui/high_contrast_textbox_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == True", Image("gui/textbox_decision_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == False", Image("gui/textbox_tall.png", yalign = 1.0, xalign = 0.5), "persistent.textbox_contrast == True and major_choice_textbox == True", Image("gui/high_contrast_textbox_decision.png", yalign = 1.0, xalign = 0.5), "persistent.textbox_contrast == True and major_choice_textbox == False", Image("gui/high_contrast_textbox.png", yalign = 1.0, xalign = 0.5), "major_choice_textbox == True", Image("gui/textbox_decision.png", yalign = 1.0, xalign = 0.5), "major_choice_textbox == False", Image("gui/textbox.png", yalign = 1.0, xalign = 0.5))
    #else:
    #    background Image("gui/textbox_short.png", xalign=0.5, yalign=.97)



translate russian style window_character:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    #if renpy.get_screen("choice"):
    background ConditionSwitch("(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == True and persistent.textbox_contrast == True", Image("gui/high_contrast_textbox_character_decision_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == False and persistent.textbox_contrast == True", Image("gui/high_contrast_textbox_character_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == True", Image("gui/textbox_character_decision_tall.png", yalign = 1.0, xalign = 0.5), "(textbox_big == True or _ru_choice_reserve_tall()) and major_choice_textbox == False", Image("gui/textbox_character_tall.png", yalign = 1.0, xalign = 0.5), "persistent.textbox_contrast == True and major_choice_textbox == True", Image("gui/high_contrast_textbox_character_decision.png", yalign = 1.0, xalign = 0.5), "persistent.textbox_contrast == True and major_choice_textbox == False", Image("gui/high_contrast_textbox_character.png", yalign = 1.0, xalign = 0.5), "major_choice_textbox == True", Image("gui/textbox_character_decision.png", yalign = 1.0, xalign = 0.5), "major_choice_textbox == False", Image("gui/textbox_character.png", yalign = 1.0, xalign = 0.5))
    #else:
    #    background Image("gui/textbox_character_short.png", xalign=0.5, yalign=.97)



screen choice(items):
    variant "ru_pilot"
    if choice_witch_override:
        if special_action:
            style_prefix "choice_snip"
        else:
            style_prefix "choice_witch"
    else:
        style_prefix "choice"
        
    default yadj = ui.adjustment()
    default choice_dialogue_length = 100
    default choice_fed_string = ""
    $ choice_fed_string = _history_list[-1].what
    $ choice_dialogue_length = len(choice_fed_string)
    key "K_UP" action ScrollViewport(yadj, 'up')
    key "K_DOWN" action ScrollViewport(yadj, 'down')
    key "pad_lefty_neg" action ScrollViewport(yadj, 'up')
    key "pad_dpup_press" action ScrollViewport(yadj, 'up')
    key "pad_dpdown_press" action ScrollViewport(yadj, 'down')
    key "pad_lefty_pos" action ScrollViewport(yadj, 'down')

    
    #text "[choice_fed_string]" ypos 200 xalign 0.5
    #text "[choice_dialogue_length]" ypos 400 xalign 0.5

    # Add yadj to viewport
    #if line_length <= 93:
    #$ choice_dialogue_length = len(str(_history_list[-1].what))
    on "show" action SetVariable("dialogue_length", len(_history_list[-1].what))
    if persistent.big_choices:
        if choice_witch_override:
            on "show" action SetVariable ("textbox_big", False)
        elif len(items) > 4 and choice_dialogue_length < 100:
            on "show" action SetVariable ("textbox_big", True)
        elif len(items) > 3 and choice_dialogue_length >= 100:
            on "show" action SetVariable ("textbox_big", True)
        else:
            on "show" action SetVariable ("textbox_big", False)
    #$ SetVariable("dialogue_length", len(_history_list[-1].what))
    #$ dialogue_length = len(_history_list[-1].what)
    if choice_witch_override == False:
        if forced_short or choice_dialogue_length < 100:
            if len(items) >= 4:
                if textbox_big:
                    viewport yadjustment yadj:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (260 if _ru_choice_reserve_tall() else 330)
                        xpos 300
                        ypos (740 if _ru_choice_reserve_tall() else 625)
                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]
                else:
                    viewport yadjustment yadj:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (210 if _ru_choice_reserve_tall() else 195)
                        xpos 300
                        ypos (790 if _ru_choice_reserve_tall() else 812)

                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]

                        


            else:
                viewport yadjustment yadj:
                    draggable False
                    mousewheel True
                    scrollbars "vertical"
                    xsize 1250
                    ysize (210 if _ru_choice_reserve_tall() else 195)
                    xpos 300
                    ypos (790 if _ru_choice_reserve_tall() else 812)
                    vbox:
                        for idx, i in enumerate(items):
                            if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                            elif idx == 0:
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                            else:
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]

        elif choice_dialogue_length >= 100:
            if len(items) > 3:
                if textbox_big:
                        
                    viewport yadjustment yadj:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (260 if _ru_choice_reserve_tall() else 300)
                        xpos 300
                        ypos (740 if _ru_choice_reserve_tall() else 690)

                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]


                            
                else:
                    viewport yadjustment yadj:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (210 if _ru_choice_reserve_tall() else 148)
                        xpos 300
                        ypos (790 if _ru_choice_reserve_tall() else 852)

                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), SetVariable ("textbox_big", False), i.action]

                        
                if forced_short:
                    $ forced_short = False

            else:
                viewport yadjustment yadj:
                    draggable False
                    mousewheel True
                    scrollbars "vertical"
                    xsize 1250
                    ysize (210 if _ru_choice_reserve_tall() else 148)
                    xpos 300
                    ypos (790 if _ru_choice_reserve_tall() else 852)
                    vbox:
                        for idx, i in enumerate(items):
                            if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                            elif idx == 0:
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                            else:
                                textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]

                if forced_short:
                    $ forced_short = False

        else:
            if len(items) >= 3:
                if textbox_big:
                    viewport yadjustment yadj:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (260 if _ru_choice_reserve_tall() else 300)
                        xpos 300
                        ypos (740 if _ru_choice_reserve_tall() else 690)

                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]

                        
                else:
                    viewport yadjustment yadj:
                        #if persistent.accessible_font:
                        draggable False
                        mousewheel True
                        scrollbars "vertical"
                        xsize 1250
                        ysize (260 if _ru_choice_reserve_tall() else 300)
                        xpos 300
                        ypos (740 if _ru_choice_reserve_tall() else 690)

                        vbox:
                            for idx, i in enumerate(items):
                                if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                elif idx == 0:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                                else:
                                    textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]

                        
                

            else:
                vbox:
                    xpos 300
                    ypos (790 if _ru_choice_reserve_tall() else 852)
                    for idx, i in enumerate(items):
                        if idx == 0 and (GamepadExists() or renpy.variant == "steam_deck"):
                            textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                        elif idx == 0:
                            textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action] default_focus True id "default_choice"
                        else:
                            textbutton i.caption action [SetVariable ("forced_short", False), SetVariable ("textbox_big", False), i.action]
    else:
        vbox:
                for i in items:
                    textbutton i.caption action i.action


