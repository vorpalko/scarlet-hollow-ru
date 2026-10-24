# One missing original movie path in the supported build. No media is copied.
# Preserve English behavior, prior callbacks, and every unrelated resource path.

init 960 python:
    import hashlib as _ru_media_hashlib

    _ru_media_missing = "images/backgrounds/episode 1/monday_woods_climax/duke_body.webm"
    _ru_media_existing = "images/_episode 1/_bg/monday_woods_climax/duke_body.webm"
    _ru_media_expected = "4268a7fd642ba12fd6f653c11cc8e024ed12a0c7b81d65b0c6cffbccf5a694dc"
    _ru_media_verified = False
    # Installer/source gates bind the entire supported archive. This local
    # check also refuses the alias if another version/mod provides this path
    # or changes the specific target video after installation.
    if not renpy.loader.loadable(_ru_media_missing) and renpy.loader.loadable(_ru_media_existing):
        with renpy.loader.load(_ru_media_existing, tl=False) as _ru_media_stream:
            _ru_media_bytes = _ru_media_stream.read()
        _ru_media_verified = (len(_ru_media_bytes) == 2481167 and
            _ru_media_hashlib.sha256(_ru_media_bytes).hexdigest() == _ru_media_expected)
        del _ru_media_bytes

    _ru_media_previous_open = config.file_open_callback
    _ru_media_previous_loadable = config.loadable_callback

    def _ru_media_open(name):
        if _ru_media_previous_open is not None:
            result = _ru_media_previous_open(name)
            if result is not None:
                return result
        if _ru_media_verified and ru_is_active() and name == _ru_media_missing:
            return renpy.loader.load(_ru_media_existing, tl=False)
        return None

    def _ru_media_loadable(name):
        if _ru_media_previous_loadable is not None and _ru_media_previous_loadable(name):
            return True
        return bool(_ru_media_verified and ru_is_active() and name == _ru_media_missing
            and renpy.loader.loadable(_ru_media_existing))

    if _ru_media_verified:
        config.file_open_callback = _ru_media_open
        config.loadable_callback = _ru_media_loadable
