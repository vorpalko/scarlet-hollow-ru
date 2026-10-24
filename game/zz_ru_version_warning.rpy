# Read-only version advisory. Never blocks startup or changes saved game data.

init 910 python:
    import hashlib as _ru_version_hashlib
    import os as _ru_version_os
    import re as _ru_version_re
    import types as _ru_version_types

    # Module attributes are process-local, outside Ren'Py's saved/rollback store.
    _ru_version_state = _ru_version_types.ModuleType("_ru_version_state")
    _ru_version_state.status = "checking"
    _ru_version_state.build = None
    _ru_version_expected_build = "25889443"
    _ru_version_expected_archive = "1dd82e3806b3be15cd209ad5ba955ea03a996519b69f8966d379b2a86205531c"

    def _ru_check_game_version(gamedir):
        _ru_version_state.build = None
        try:
            game_root = _ru_version_os.path.dirname(gamedir)
            parent = game_root
            detected_builds = set()
            valid_metadata = True
            mismatch = False
            for _ in range(3):
                manifest = _ru_version_os.path.join(parent, "appmanifest_1609230.acf")
                if _ru_version_os.path.isfile(manifest):
                    with open(manifest, "rb") as stream:
                        text = stream.read(1024 * 1024 + 1).decode("utf-8-sig")
                    if len(text) > 1024 * 1024:
                        raise ValueError("Steam manifest too large")
                    builds = _ru_version_re.findall(r'"buildid"\s+"([^"\r\n]+)"', text, _ru_version_re.I)
                    apps = _ru_version_re.findall(r'"appid"\s+"([^"\r\n]+)"', text, _ru_version_re.I)
                    trusted = bool(builds and set(apps) == {"1609230"}
                        and all(_ru_version_re.fullmatch(r"[0-9]{1,20}", value) for value in builds))
                    valid_metadata = valid_metadata and trusted
                    if trusted:
                        detected_builds.update(builds)
                    mismatch = mismatch or set(builds) != {_ru_version_expected_build} or not trusted
                parent = _ru_version_os.path.dirname(parent)
            if valid_metadata and len(detected_builds) == 1:
                _ru_version_state.build = next(iter(detected_builds))
            if mismatch:
                _ru_version_state.status = "mismatch"
                return
            checksum = _ru_version_hashlib.sha256()
            with open(_ru_version_os.path.join(gamedir, "archive.rpa"), "rb") as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                    checksum.update(block)
            _ru_version_state.status = "match" if checksum.hexdigest() == _ru_version_expected_archive else "mismatch"
            if _ru_version_state.status == "match":
                # An exact archive identifies the audited build even in a copy
                # without Steam metadata. Never infer it from the package alone.
                _ru_version_state.build = _ru_version_expected_build
        except Exception:
            # A failed read is advisory too; it must never stop the game.
            _ru_version_state.status = "unknown"

    def _ru_version_details(russian):
        build = _ru_version_state.build
        if build:
            game = build
        elif _ru_version_state.status == "checking":
            game = "проверка…" if russian else "checking…"
        else:
            game = "не определена" if russian else "unknown"
        return (("Установлена версия " + game + "   Перевод на версию ") if russian else
                ("Installed version " + game + "   Translation for version ")) + _ru_version_expected_build

    def _ru_version_advisory(russian):
        if _ru_version_state.status == "unknown":
            return ("Не удалось проверить версию игры.\nПеревод может работать некорректно." if russian else
                    "Unable to verify the game version.\nThe translation may not work correctly.")
        return ("Версия игры отличается от версии перевода.\nВозможны ошибки и непереведённый текст." if russian else
                "Game version differs from the translation's reference version.\nErrors and untranslated text are possible.")

    config.always_shown_screens.append("ru_version_warning")
    # The multi-GB archive is read in a worker; completion refreshes the UI.
    renpy.invoke_in_thread(_ru_check_game_version, config.gamedir)

screen ru_version_warning():
    zorder 149
    if main_menu and renpy.get_screen("main_menu") and _ru_version_state.status in ("mismatch", "unknown"):
        frame:
            id "ru_version_warning_frame"
            background Solid("#291d16ed")
            padding (22, 10)
            xalign 0.5
            yalign 0.985
            xsize 1060
            vbox:
                spacing 4
                xfill True
                text _ru_version_advisory(ru_is_active()):
                    id "ru_version_warning_text"
                    font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                    size 25
                    color "#ffcb73"
                    text_align 0.5
                    xalign 0.5
                text _ru_version_details(ru_is_active()):
                    id "ru_version_details_text"
                    substitute False
                    font "ru_support/fonts/Spectral/Spectral-Regular.ttf"
                    size 23
                    color "#ffcb73"
                    text_align 0.5
                    xalign 0.5
