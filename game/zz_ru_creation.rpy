# Localized creation screens use a language variant. Original English screens remain registered.

style ru_creation_heading:
    font "gui/fonts/AmaticSC-Bold.ttf"
    size 64
    color "#2b211e"
    text_align 0.5

style ru_creation_text:
    font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
    size 30
    color "#2b211e"

style ru_creation_button:
    background Solid("#ede2c5")
    hover_background Solid("#fff3d3")
    selected_background Solid("#cab788")
    insensitive_background Solid("#c4bfb2")
    padding (24, 12)

style ru_creation_button_text is ru_creation_text:
    hover_color "#a84232"
    selected_color "#6a271f"
    insensitive_color "#716e65"
    text_align 0.5

screen input(prompt):
    variant "ru_pilot"
    default key_upper = True
    default key_language = "ru"
    default keyboard_visible = GamepadExists() and not renpy.variant("steam_deck")
    key "pad_b_press" action PostEvent("input_backspace")

    # The localized card is already selected by c_name/c_town before fade.
    window:
        background None
        style "nvl_window"
        input id "input" xalign 0.5 yalign 0.5 size 50 font "gui/fonts/PT Mono Regular.ttf"
    textbutton ("Скрыть клавиатуру" if keyboard_visible else "Экранная клавиатура"):
        style "ru_creation_button"
        text_style "ru_creation_button_text"
        xalign 0.5
        ypos 710
        action ToggleScreenVariable("keyboard_visible")
    if keyboard_visible:
        frame:
            background Solid("#e5d9bbf5")
            padding (20, 14)
            xalign 0.5
            ypos 785
            vbox:
                spacing 8
                $ letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" if key_language == "ru" else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                grid 11 3:
                    spacing 5
                    for letter in letters:
                        textbutton (letter if key_upper else letter.lower()):
                            style "ru_creation_button"
                            text_style "ru_creation_button_text"
                            text_size 25
                            xsize 64
                            ysize 49
                            padding (4, 2)
                            action [EmulateKeyboard(letter if key_upper else letter.lower()), SetScreenVariable("key_upper", False)]
                    for filler in range(33 - len(letters)):
                        null
                hbox:
                    spacing 7
                    for caption, action in (
                        ("RU / EN", ToggleScreenVariable("key_language", "ru", "en")),
                        ("Аа", ToggleScreenVariable("key_upper")),
                        ("Пробел", EmulateKeyboard(" ")),
                        ("Стереть", PostEvent("input_backspace")),
                        ("Готово", PostEvent("input_enter"))):
                        textbutton caption style "ru_creation_button" text_style "ru_creation_button_text" text_size 24 action action

screen gender():
    variant "ru_pilot"

    text _("{color=#FFFFFF00}Select your pronouns and hit confirm. You can navigate these buttons using the arrow keys to hover and enter to select. Confirm won't be hoverable until you've selected an option.{/color}")
    add ru_graphic("gui/gender/gender_idle.png") xpos 741 ypos 36

    for value, icon, caption, x in (("male", "male", "He him", 406), ("enby", "enby", "They them", 873), ("female", "female", "She her", 1340)):
        imagebutton:
            alt _(caption)
            idle ru_graphic("gui/gender/" + icon + "_idle.png")
            hover ru_graphic("gui/gender/" + icon + "_hover.png")
            selected_idle ru_graphic("gui/gender/" + icon + "_selected_idle.png")
            selected_hover ru_graphic("gui/gender/" + icon + "_selected_hover.png")
            xpos x
            ypos 330
            sensitive not selected_gender or gender == value
            selected gender == value
            action [Play("audio", "audio/one_shot/furniture_budge.wav"), SetVariable("gender", "undecided" if gender == value else value), SetVariable("selected_gender", not selected_gender)]

    imagebutton:
        alt _("Confirm")
        idle ru_graphic("gui/confirm_idle.png")
        hover ru_graphic("gui/confirm_hover.png")
        xpos 831
        ypos 927
        sensitive selected_gender
        action [Play("audio", "audio/one_shot/furniture_budge.wav"), Jump("traits")]

screen ru_trait_choices(limit):
    if limit == 2:
        text _("{color=#FFFFFF00}Select two traits and hit confirm. Traits will give you additional dialogue options and story routes. You can navigate these buttons using the arrow keys and enter to select. Confirm won't be hoverable until you've selected two traits.{/color}")
        add ru_graphic("gui/traits/traits_idle.png") xpos 741 ypos 36
    else:
        text _("{color=#FFFFFF00}Select three traits and hit confirm. Traits will give you additional dialogue options and story routes. You can navigate these buttons using the arrow keys and enter to select. Confirm won't be hoverable until you've selected three traits.{/color}")
        add ru_graphic("gui/traits/traits_hardcore_idle.png") xpos 741 ypos 36

    for key, art, description, x, y in (
        ("powerful_build", "powerful", "Powerful Build. Tough, Intimidating, the Pinnacle of Fitness", 214, 230),
        ("mystical", "mystic", "Mystical. Strange and unusual. Can see the threads of reality in a way others cannot.", 607, 230),
        ("animals", "animals", "Talk to Animals. You can talk to animals. Animals can talk to you. A blessing and a curse.", 1000, 230),
        ("street_smart", "street", "Street Smart. Good at lying and hard to lie to. Fast talker. No door can hold you.", 1393, 230),
        ("keen_eye", "keen", "Keen Eye. Observant with a knack for picking up details. Empathetic.", 411, 586),
        ("book_smart", "book", "Book Smart. Well read and rational. Possess a wealth of esoteric knowledge and know when to use it.", 804, 586),
        ("hot", "hot", "Hot. Extremely good looking. A natural flirt. People are nice to you, probably because you're a good person.", 1197, 586)):
        imagebutton:
            alt _(description)
            idle ru_graphic("gui/traits/" + art + "_idle.png")
            hover ru_graphic("gui/traits/" + art + "_hover.png")
            selected_idle ru_graphic("gui/traits/" + art + "_selected_idle.png")
            selected_hover ru_graphic("gui/traits/" + art + "_selected_hover.png")
            xpos x
            ypos y
            selected getattr(renpy.store, key)
            sensitive selected_traits < limit or getattr(renpy.store, key)
            action [Play("audio", "audio/one_shot/furniture_budge.wav"), Function(_ru_toggle_trait, key, limit)]

    imagebutton:
        alt _("Confirm.")
        idle ru_graphic("gui/confirm_idle.png")
        hover ru_graphic("gui/confirm_hover.png")
        xpos 831
        ypos 927
        sensitive selected_traits == limit
        action [Play("audio", "audio/one_shot/furniture_budge.wav"), Jump("bus")]

screen traits():
    variant "ru_pilot"
    use ru_trait_choices(2)

screen traits_hardcore():
    variant "ru_pilot"
    use ru_trait_choices(3)
