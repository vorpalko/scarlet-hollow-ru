# Russian pilot support. Original story state and English pronoun dictionary stay intact.

init 900 python:
    _ru_font_root = "ru_support/fonts/Spectral/"
    _ru_font_faces = {
        (False, False): _ru_font_root + "Spectral-Regular.ttf",
        (False, True): _ru_font_root + "Spectral-Italic.ttf",
        (True, False): _ru_font_root + "Spectral-Bold.ttf",
        (True, True): _ru_font_root + "Spectral-BoldItalic.ttf",
    }
    _ru_font_targets = {}
    for _ru_bold in (False, True):
        for _ru_italic in (False, True):
            _ru_font_targets[("gui/fonts/KelmscottRomanNF.ttf", _ru_bold, _ru_italic)] = (
                _ru_font_faces[(_ru_bold, _ru_italic)], False, False)
            for _ru_old, _ru_new in (
                ("gui/fonts/Courier Prime.ttf", "gui/fonts/PT Mono Regular.ttf"),
                ("gui/fonts/EastSeaDokdo-Regular.ttf", "gui/fonts/AmaticSC-Bold.ttf"),
                ("gui/fonts/NothingYouCouldDo-Regular.ttf", "gui/fonts/AmaticSC-Regular.ttf"),
                ("gui/fonts/RockSalt-Regular.ttf", "gui/fonts/AmaticSC-Bold.ttf"),
            ):
                _ru_font_targets[(_ru_old, _ru_bold, _ru_italic)] = (_ru_new, _ru_bold, _ru_italic)

    _ru_original_font_entries = {
        key: config.font_replacement_map[key]
        for key in _ru_font_targets if key in config.font_replacement_map
    }

    def ru_is_active():
        return renpy.game.preferences.language == "russian"

    def _ru_language_hotkey_allowed():
        if any(renpy.get_screen(name) for name in
               ("input", "save", "load", "confirm", "_console", "_developer")):
            return False
        return bool(not main_menu and not getattr(renpy.context(), "_menu", False)
                    and (renpy.get_screen("say") or renpy.get_screen("choice")))

    def _ru_language_setup():
        # New filenames prevent the 8.0.3 face cache from retaining the wrong alphabet.
        if ru_is_active():
            config.font_replacement_map.update(_ru_font_targets)
            if "ru_pilot" not in config.variants:
                config.variants.insert(0, "ru_pilot")
        else:
            for key, value in _ru_font_targets.items():
                if config.font_replacement_map.get(key) == value:
                    if key in _ru_original_font_entries:
                        config.font_replacement_map[key] = _ru_original_font_entries[key]
                    else:
                        config.font_replacement_map.pop(key, None)
            config.variants[:] = [v for v in config.variants if v != "ru_pilot"]

    def ru_form(male, female, neutral):
        """Select a full contextual form without mutating save or story data."""
        return {"male": male, "female": female}.get(getattr(renpy.store, "gender", "undecided"), neutral)

    def ru_pronoun(case="nom", capital=False):
        forms = {
            "male": {"nom": "он", "gen": "его", "dat": "ему", "acc": "его", "inst": "им", "prep": "нём", "poss": "его"},
            "female": {"nom": "она", "gen": "её", "dat": "ей", "acc": "её", "inst": "ею", "prep": "ней", "poss": "её"},
            "enby": {"nom": "они", "gen": "их", "dat": "им", "acc": "их", "inst": "ими", "prep": "них", "poss": "их"},
        }
        value = forms.get(getattr(renpy.store, "gender", "undecided"), forms["enby"])[case]
        return value.capitalize() if capital else value

    _ru_trait_keys = ("powerful_build", "mystical", "animals", "street_smart", "keen_eye", "book_smart", "hot")

    def _ru_toggle_trait(key, limit):
        if key not in _ru_trait_keys or limit not in (2, 3):
            return
        selected = bool(getattr(renpy.store, key))
        count = sum(bool(getattr(renpy.store, k)) for k in _ru_trait_keys)
        if selected or count < limit:
            setattr(renpy.store, key, not selected)
            renpy.store.selected_traits = sum(bool(getattr(renpy.store, k)) for k in _ru_trait_keys)
            renpy.restart_interaction()

    config.change_language_callbacks.append(_ru_language_setup)
    config.always_shown_screens.append("ru_pilot_language_selector")
    config.always_shown_screens.append("ru_language_hotkey")

screen ru_language_hotkey():
    zorder 150
    modal _ru_preview_active()
    if _ru_language_hotkey_allowed():
        key "K_q" action Function(_ru_preview_toggle)
    if _ru_preview_active():
        key "game_menu" action Function(_ru_preview_close)
        key "rollback" action Function(_ru_preview_close)
        key "rollforward" action Function(_ru_preview_close)
        frame:
            background Solid("#211a19fa")
            padding (28, 22)
            xalign 0.5
            yalign 0.97
            xsize 1620
            ysize 730
            vbox:
                spacing 16
                hbox:
                    xfill True
                    text ("Русский" if _ru_preview_data()["target"] == "russian" else "English"):
                        font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                        size 30
                        color "#eee1cd"
                    null width 30
                    text ("Q / Esc — вернуться" if ru_is_active() else "Q / Esc — return"):
                        font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                        size 26
                        color "#bcae9c"
                    textbutton ("Закрыть" if ru_is_active() else "Close"):
                        text_font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                        text_size 26
                        action Function(_ru_preview_close)
                viewport:
                    id "ru_preview_viewport"
                    xsize 1564
                    ysize 620
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        spacing 18
                        xsize 1500
                        if _ru_preview_data()["who"]:
                            text _ru_preview_data()["who"]:
                                substitute False
                                font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                                size 30
                                bold True
                                color "#d7bba5"
                        text _ru_preview_data()["what"]:
                            id "ru_preview_what"
                            substitute False
                            font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                            size 32
                            color "#eee1cd"
                            slow_cps 0
                        for _ru_index, _ru_item in enumerate(_ru_preview_data()["items"]):
                            button:
                                xsize 1480
                                padding (12, 8)
                                sensitive _ru_item["sensitive"]
                                action Function(_ru_preview_choose, _ru_index)
                                text _ru_item["caption"]:
                                    substitute False
                                    style "button_text"
                                    font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                                    size 30
                                    color "#ddd5c7"
                                    hover_color "#ffffff"
    if renpy.get_screen("preferences"):
        frame:
            background Solid("#211a19e8")
            padding (20, 12)
            xalign 0.98
            yalign 0.98
            text ("Q / Й — реплики и ответы на другом языке" if ru_is_active() else "Q / Й — dialogue and choices in the other language"):
                font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                size 26
                color "#ddd5c7"

screen ru_pilot_language_selector():
    zorder 150
    if main_menu and renpy.get_screen("main_menu"):
        frame:
            background Solid("#211a19e8")
            padding (20, 12)
            xalign 0.98
            yalign 0.98
            hbox:
                spacing 20
                textbutton "English":
                    text_font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                    text_size 26
                    text_color "#ddd5c7"
                    text_selected_color "#ffffff"
                    selected not ru_is_active()
                    action Language(None)
                textbutton "Русский":
                    text_font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                    text_size 26
                    text_color "#ddd5c7"
                    text_selected_color "#ffffff"
                    selected ru_is_active()
                    action Language("russian")

translate russian style say_dialogue:
    line_spacing 2

# Episode 5's dedicated cinematic captions share this otherwise unused style.
# Keep the native type size and 220px window; use its available width and
# reserve space above/below the full caption, including the native CTC arrow.
translate russian style window_flashback:
    xsize 1920
    background Solid("#000000")

translate russian style voice_style:
    xpos 0.5
    xanchor 0.5
    xsize 1760
    ypos 12

translate russian style input:
    font "gui/fonts/PT Mono Regular.ttf"

translate russian style navigation_button_text:
    size 32

# Match the original menu's 58-pixel rows and 64-pixel baseline pitch. Spectral
# has a taller em box than Kelmscott even when its visible letters are smaller.
# Keep a larger optical size inside the original row instead of spacing by em.
translate russian style mainmenu_button:
    ysize 58
    padding (6, 0)

translate russian style mainmenu_button_text:
    size 38
    yalign 0.5

translate russian style pref_label_text:
    line_spacing 2

# Spectral's line box is taller than Kelmscott's. Remove redundant vertical
# button padding and tighten label margins so all preferences, including the
# mute toggle, fit above the bottom frame at the original text sizes.
translate russian style pref_label:
    top_margin 10

translate russian style radio_button:
    top_padding 0
    bottom_padding 0

translate russian style check_button:
    top_padding 0
    bottom_padding 0

# Preview data lives on the engine module, outside store/rollback/save data.
# No engine function is replaced and no language preference is changed.
init 902 python:
    import types as _ru_preview_types
    import threading as _ru_preview_threading
    import re as _ru_preview_re

    renpy._sh_ru_text_preview = _ru_preview_types.SimpleNamespace(
        pairs={}, raw={}, contexts={}, active=False, data=None, format=_ru_preview_threading.local(), stats={}, afm_callback=None)

    def _ru_preview_state():
        return renpy._sh_ru_text_preview

    def ru_text_is_active():
        """Only pure text helpers consult this formatter-local language."""
        return getattr(_ru_preview_state().format, "language", renpy.game.preferences.language) == "russian"

    class _RuPreviewFormatter(renpy.substitutions.Formatter):
        def __init__(self, language):
            self.language = language

        def convert_field(self, value, conversion):
            if conversion and "t" in conversion:
                obj, scope = value
                if "r" in conversion:
                    obj = repr(obj)
                elif "s" in conversion:
                    obj = str(obj)
                obj = renpy.translate_string(str(obj), language=self.language)
                rest = conversion.replace("r", "").replace("s", "").replace("t", "")
                return super(_RuPreviewFormatter, self).convert_field((obj, scope), rest) if rest else obj
            return super(_RuPreviewFormatter, self).convert_field(value, conversion)

    def _ru_preview_format(text, language):
        state = _ru_preview_state()
        local = state.format
        had = hasattr(local, "language")
        previous = getattr(local, "language", None)
        local.language = language
        try:
            text = renpy.translate_string(text, language=language)
            return _RuPreviewFormatter(language).vformat(text, (), renpy.store.__dict__)
        finally:
            if had:
                local.language = previous
            else:
                del local.language

    def _ru_preview_reset():
        state = _ru_preview_state()
        state.active = False
        state.data = None
        state.contexts.clear()

    def _ru_preview_raw_pair(raw, who=None, context=None):
        state = _ru_preview_state()
        base = 1 if ru_is_active() else 0
        ctx = context or renpy.game.context()
        captured = state.contexts.get(id(ctx))
        if captured and captured[base] == raw:
            return captured
        # Read exact saved AST provenance first, including the deferred Say above
        # a menu. Never select a translation from a rendered-string reverse map.
        node = renpy.game.script.namemap.get(ctx.current)
        pair = state.pairs.get(getattr(node, "name", None))
        if pair and pair[base] == raw:
            return pair
        tid = ctx.translate_identifier or ctx.deferred_translate_identifier
        original = renpy.game.script.translator.default_translates.get(tid)
        if original:
            for statement in original.block:
                pair = state.pairs.get(statement.name)
                if pair and pair[base] == raw:
                    return pair
        candidates = state.raw.get(raw, ())
        if who is not None:
            candidates = [p for p in candidates if p[2] == who or p[3] == who]
        distinct = set(candidates)
        if len(distinct) == 1:
            return next(iter(distinct))
        # History stores an exact rollback-entry identifier. Its saved context
        # disambiguates repeated source text without performing any rollback.
        history = getattr(renpy.store, "_history_list", ())
        if history:
            identifier = getattr(history[-1], "rollback_identifier", None)
            log = renpy.game.log
            entries = list(getattr(log, "log", ()))
            current = getattr(log, "current", None)
            if current is not None:
                entries.append(current)
            for entry in reversed(entries):
                if entry.identifier == identifier and entry.context is not ctx:
                    saved = entry.context
                    saved_node = renpy.game.script.namemap.get(saved.current)
                    exact = state.pairs.get(getattr(saved_node, "name", None))
                    if exact and exact[base] == raw:
                        return exact
        marker = config.extend_interjection
        if marker and marker in raw:
            prefix, suffix = raw.rsplit(marker, 1)
            before = _ru_preview_raw_pair(prefix, who, ctx)
            after = _ru_preview_raw_pair(suffix, "extend", ctx)
            if before and after:
                return (before[0] + marker + after[0], before[1] + marker + after[1], before[2], before[3])
        return None

    def _ru_preview_statement(name):
        state = _ru_preview_state()
        state.active = False
        state.data = None
        ctx = renpy.game.context()
        node = renpy.game.script.namemap.get(ctx.current)
        if not isinstance(node, renpy.ast.Say):
            return
        pair = state.pairs.get(node.name)
        if pair is None:
            return
        if node.who == "extend":
            before = _ru_preview_raw_pair(getattr(renpy.store, "_last_say_what", ""),
                                          getattr(renpy.store, "_last_say_who", None), ctx)
            if before is None:
                state.contexts.pop(id(ctx), None)
                return
            marker = config.extend_interjection
            pair = (before[0] + marker + pair[0], before[1] + marker + pair[1], before[2], before[3])
        state.contexts[id(ctx)] = pair

    def _ru_preview_active():
        state = _ru_preview_state()
        return bool(state.active and state.data and _ru_language_hotkey_allowed()
                    and state.data["context"] == (id(renpy.game.context()), renpy.game.context().current))

    def _ru_preview_data():
        return _ru_preview_state().data

    def _ru_preview_afm_callback():
        # AFM also checks non-timer events in Ren'Py 8.0.3. Keep the native
        # voice callback, but pause automatic advancement while reading.
        if _ru_preview_active():
            return False
        callback = _ru_preview_state().afm_callback
        return callback() if callback is not None else True

    def _ru_preview_close():
        state = _ru_preview_state()
        state.active = False
        state.data = None
        renpy.restart_interaction()

    def _ru_preview_contains(action, target):
        if action is target:
            return True
        if isinstance(action, (list, tuple)):
            return any(_ru_preview_contains(a, target) for a in action)
        return False

    def _ru_preview_native_buttons(screen):
        buttons = []
        if screen is not None and screen.child is not None:
            screen.child.visit_all(lambda d: buttons.append(d) if isinstance(d, renpy.display.behavior.Button) else None)
        return buttons

    def _ru_preview_sensitive(screen, button):
        renpy.display.screen.push_current_screen(screen)
        try:
            return bool(button.is_sensitive())
        finally:
            renpy.display.screen.pop_current_screen()

    def _ru_preview_choose(index):
        if not _ru_preview_active():
            return
        data = _ru_preview_data()
        screen = renpy.get_screen("choice")
        if screen is not data["choice_screen"] or not 0 <= index < len(data["items"]):
            return
        entry = data["items"][index]
        buttons = [b for b in _ru_preview_native_buttons(screen) if _ru_preview_contains(b.action, entry["item_action"])]
        if len(buttons) != 1 or not _ru_preview_sensitive(screen, buttons[0]):
            return
        _ru_preview_state().active = False
        _ru_preview_state().data = None
        renpy.display.screen.push_current_screen(screen)
        try:
            return renpy.run(buttons[0].action)
        finally:
            renpy.display.screen.pop_current_screen()

    def _ru_preview_toggle():
        if not _ru_language_hotkey_allowed():
            return
        if _ru_preview_active():
            return _ru_preview_close()
        state = _ru_preview_state()
        language = None if ru_is_active() else "russian"
        base = 1 if ru_is_active() else 0
        target = 1 - base
        say = renpy.get_screen("say")
        if say is not None and (getattr(say, "hiding", False) or "what" in getattr(say, "hidden_widgets", {})):
            say = None
        raw = getattr(renpy.store, "_last_say_what", "")
        node = renpy.game.script.namemap.get(renpy.game.context().current)
        if isinstance(node, renpy.ast.Say) and node.who == "extend":
            raw += config.extend_interjection + node.what
        pair = _ru_preview_raw_pair(raw, getattr(renpy.store, "_last_say_who", None))
        choice = renpy.get_screen("choice")
        if say is not None and pair is None:
            # An unbound custom display must never be given an unrelated line.
            renpy.notify("Для этого текста нет точной пары перевода." if ru_is_active() else "No exact text pair is available.")
            return
        body = _ru_preview_format(pair[target], language) if say is not None else ""
        # Text control tags belong to the underlying dialogue interaction. The
        # read-only preview shows the full current Say without pause/dismiss.
        body = _ru_preview_re.sub(r"\{(?:w|p|nw|fast|done)(?:=[^}]*)?\}", "", body) + "{fast}"
        who = say.scope.get("who") if say is not None else None
        ref = pair[target + 2] if pair else None
        character = (renpy.store.narrator if ref is None else renpy.store.__dict__.get(ref)) if say is not None else None
        if isinstance(character, renpy.character.ADVCharacter) and not character.dynamic:
            who = character.name
        elif character is not None and getattr(character, "dynamic", False) and isinstance(character.name, str):
            who = renpy.python.py_eval(character.name)
        if who is not None:
            who = _ru_preview_format(who, language)
            if isinstance(character, renpy.character.ADVCharacter):
                who = _ru_preview_format(character.who_prefix, language) + who + _ru_preview_format(character.who_suffix, language)
        if isinstance(character, renpy.character.ADVCharacter):
            body = _ru_preview_format(character.what_prefix, language) + body + _ru_preview_format(character.what_suffix, language)
        items = []
        if choice is not None:
            native = _ru_preview_native_buttons(choice)
            for item in choice.scope.get("items", ()):
                buttons = [b for b in native if _ru_preview_contains(b.action, item.action)]
                if len(buttons) != 1:
                    return
                items.append({"caption": _ru_preview_format(item.caption, language),
                              "item_action": item.action, "sensitive": _ru_preview_sensitive(choice, buttons[0])})
        state.data = {"target": language, "what": body, "who": who, "items": items,
                      "context": (id(renpy.game.context()), renpy.game.context().current), "choice_screen": choice}
        state.active = True
        renpy.restart_interaction()

    config.statement_callbacks.append(_ru_preview_statement)
    config.after_load_callbacks.append(_ru_preview_reset)

init 950 python:
    _ru_preview_state().afm_callback = config.afm_callback
    config.afm_callback = _ru_preview_afm_callback
    _ru_preview_translator = renpy.game.script.translator
    _ru_preview_pairs_count = 0
    _ru_preview_unmatched = []
    for _ru_preview_id, _ru_preview_original in _ru_preview_translator.default_translates.items():
        _ru_preview_russian = _ru_preview_translator.language_translates.get((_ru_preview_id, "russian"), _ru_preview_original)
        _ru_preview_en_says = [s for s in _ru_preview_original.block if isinstance(s, renpy.ast.Say)]
        _ru_preview_ru_says = [s for s in _ru_preview_russian.block if isinstance(s, renpy.ast.Say)]
        if len(_ru_preview_en_says) != len(_ru_preview_ru_says):
            _ru_preview_unmatched.append(_ru_preview_id)
            continue
        for _ru_preview_en, _ru_preview_ru in zip(_ru_preview_en_says, _ru_preview_ru_says):
            _ru_preview_pair = (_ru_preview_en.what, _ru_preview_ru.what, _ru_preview_en.who, _ru_preview_ru.who)
            _ru_preview_state().pairs[_ru_preview_en.name] = _ru_preview_pair
            _ru_preview_state().pairs[_ru_preview_ru.name] = _ru_preview_pair
            for _ru_preview_raw in set(_ru_preview_pair[:2]):
                _ru_preview_state().raw.setdefault(_ru_preview_raw, set()).add(_ru_preview_pair)
            _ru_preview_pairs_count += 1
    _ru_preview_state().stats = {"paired_says": _ru_preview_pairs_count, "unmatched_blocks": tuple(_ru_preview_unmatched)}
