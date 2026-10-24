# Localized pictogram accessibility, shared journal art and Episodes 1–3 entries.
# Original journal actions and conditions remain intact; translated columns scroll.

screen quick_menu():
    variant "ru_pilot"
    zorder 100
    if quick_menu:
        vbox:
            style_prefix "quick"
            spacing 15
            ypos 765
            xpos 1609
            imagebutton:
                auto "gui/Quick Menu/convo_%s.png"
                alt "История диалогов"
                action [Play("audio", "audio/one_shot/furniture_budge.wav"), ShowMenu("history")]
            imagebutton:
                auto "gui/Quick Menu/journal_%s.png"
                alt "Журнал"
                action [Show("journal", dissolve), Play("audio", "audio/one_shot/pack_search_short.wav"), SetVariable("visible_page", 1)]
            imagebutton:
                auto "gui/Quick Menu/save_%s.png"
                alt "Сохранить"
                action [Play("audio", "audio/one_shot/furniture_budge.wav"), ShowMenu("save")]
            imagebutton:
                auto "gui/Quick Menu/options_%s.png"
                alt "Настройки"
                action [Play("audio", "audio/one_shot/furniture_budge.wav"), ShowMenu("preferences")]

screen _ru_journal_episode1_viewport():
    viewport:
        xpos 560
        ypos 131
        xysize (580, 850)
        mousewheel True
        draggable True
        arrowkeys True
        pagekeys True
        scrollbars "vertical"
        null

screen _ru_journal_episode2_viewport():
    viewport:
        xpos 1240
        ypos 131
        xysize (580, 850)
        mousewheel True
        draggable True
        arrowkeys True
        pagekeys True
        scrollbars "vertical"
        null

init 960 python:
    import ast as _ru_journal_ast
    import copy as _ru_journal_copy

    class _RuJournalViewport(renpy.display.viewport.Viewport):
        # Native8.0.3 Viewport handles arrows/pages without checking focus;
        # wheel-up/down also map to arrows. Filter before the native handler,
        # including its wheel branch, so an inactive column cannot steal keys.
        def _ru_journal_keyboard_active(self):
            focused = renpy.display.focus.get_grab() or renpy.display.focus.get_focused()
            if (focused is self or
                    (focused is not None and
                     (getattr(focused, "adjustment", None) is self.xadjustment or
                      getattr(focused, "adjustment", None) is self.yadjustment))):
                return True
            # Keep native single-column keyboard behavior, including an early
            # E1 page in the cumulative package. Inspect displayed widgets only;
            # no story flag or saved/default selection is changed or cached.
            screen = renpy.get_screen("journal")
            visible = set()
            if screen is not None and screen.child is not None:
                screen.child.visit_all(lambda d: visible.add(id(d)) if isinstance(d, _RuJournalViewport) else None)
            return visible == {id(self)}

        def event(self, ev, x, y, st):
            keyboard_scroll = (
                self.arrowkeys and any(renpy.display.behavior.map_event(ev, key) for key in (
                    "viewport_leftarrow", "viewport_rightarrow", "viewport_uparrow", "viewport_downarrow"))
                or self.pagekeys and any(renpy.display.behavior.map_event(ev, key) for key in (
                    "viewport_pageup", "viewport_pagedown")))
            if keyboard_scroll and not self._ru_journal_keyboard_active():
                return None
            return super(_RuJournalViewport, self).event(ev, x, y, st)

    # Private constructors only. Neither renpy.ui.viewport nor the parser/global
    # Viewport class is changed. Keep native scrollbar/side/style/replaces logic.
    def _ru_journal_sl2viewport(context=None, **kwargs):
        detached = renpy.ui.detached()
        if context is not None:
            renpy.ui.stack[-1].style_prefix = context.style_prefix
        # Wrapper serializes by its renpy.ui global name. This private unnamed
        # instance is ephemeral, never stored in the screen tree or store.
        constructor = renpy.ui.Wrapper(
            _RuJournalViewport, one=True, replaces=True, style="viewport")
        viewport = renpy.ui.viewport_common(constructor, True, **kwargs)
        renpy.ui.stack.pop()
        result = detached.child
        if viewport is not result:
            result._main = viewport
        result._composite_parts = list(result.children)
        return result

    _ru_journal_sources = {}
    for _ru_journal_key in ("powerful", "mystical", "animals", "street", "keen", "book", "hot"):
        _ru_journal_art_key = "mystic" if _ru_journal_key == "mystical" else _ru_journal_key
        for _ru_journal_family, _ru_journal_size in (("traits", 160), ("hardcore_traits", 120)):
            _ru_journal_sources["gui/journal/" + _ru_journal_family + "/" + _ru_journal_key + "_journal.png"] = (
                "gui/traits/" + _ru_journal_art_key + "_idle.png", _ru_journal_size)
    _ru_journal_sources["gui/journal/buttons/return idle.png"] = ("gui/journal/buttons/return idle.png", None)
    _ru_journal_sources["gui/journal/buttons/return hover.png"] = ("gui/journal/buttons/return idle.png", None)
    _ru_journal_cache = {}

    def _ru_journal_graphic(source):
        # These are shared trait/return assets. Narrative pages after the
        # translated episodes keep their original text.
        if not ru_is_active():
            return Image(source)
        if source not in _ru_journal_cache:
            # Each journal state supplies its own original drawing and rim.
            # Only lettering crops are shared with the creation family.
            _ru_journal_cache[source] = ru_graphic(source)
        return _ru_journal_cache[source]

    # Clone only the screen-language tree in memory. This neither republishes
    # extracted story source nor patches the English tree or archived scripts.
    # Only the finite image/text expressions change. Original Python statements
    # retain their compiled code: PyCode.__getstate__ drops bytecode on deepcopy,
    # and a clone created during init is too late for the script compilation pass.
    _ru_original_journal = renpy.display.screen.screens[("journal", None)]
    if not isinstance(_ru_original_journal.function, renpy.sl2.slast.SLScreen):
        raise Exception("Russian journal requires the supported native SL2 screen")
    _ru_journal_code_memo = {}

    def _ru_journal_keep_compiled_code(node):
        code = getattr(node, "code", None)
        if code is not None:
            _ru_journal_code_memo[id(code)] = code
        for child in getattr(node, "children", ()):
            _ru_journal_keep_compiled_code(child)
        for _condition, block in getattr(node, "entries", ()):
            _ru_journal_keep_compiled_code(block)

    _ru_journal_keep_compiled_code(_ru_original_journal.function)
    _ru_journal_screen = _ru_journal_copy.deepcopy(_ru_original_journal.function, _ru_journal_code_memo)
    _ru_journal_replacements = {}
    _ru_journal_text_replacements = {}

    def _ru_journal_replace_expression(expression):
        try:
            value = _ru_journal_ast.literal_eval(expression)
        except (ValueError, SyntaxError, TypeError):
            return expression
        if not isinstance(value, str):
            return expression
        if value in _ru_journal_texts:
            _ru_journal_text_replacements[value] = _ru_journal_text_replacements.get(value, 0) + 1
            return "_ru_journal_text(" + repr(value) + ")"
        if value not in _ru_journal_sources:
            return expression
        _ru_journal_replacements[value] = _ru_journal_replacements.get(value, 0) + 1
        return "_ru_journal_graphic(" + repr(value) + ")"

    def _ru_journal_rewrite(node):
        if isinstance(node, renpy.sl2.slast.SLDisplayable):
            node.positional = [_ru_journal_replace_expression(expr) for expr in node.positional]
            node.keyword = [(key, _ru_journal_replace_expression(expr)) for key, expr in node.keyword]
        for child in getattr(node, "children", ()):
            _ru_journal_rewrite(child)
        for _condition, block in getattr(node, "entries", ()):
            _ru_journal_rewrite(block)

    _ru_journal_rewrite(_ru_journal_screen)
    if set(_ru_journal_replacements) != set(_ru_journal_sources):
        raise Exception("Russian journal asset expressions differ from the supported source")
    if set(_ru_journal_text_replacements) != set(_ru_journal_texts) or any(
            count != 1 for count in _ru_journal_text_replacements.values()):
        raise Exception("Russian journal text differs from the supported source")

    # The original fixed page cannot fit long Russian decision histories.
    # Preserve every condition and Python statement; put each exact translated
    # episode block in its own scrollable page and retain the original vbox flow.
    _ru_journal_headers = {
        "_ru_journal_text(" + repr("{size=36}{u}Monday – Major Decisions{/u}{/size}") + ")": "_ru_journal_episode1_viewport",
    }
    if "_ru_episode2_journal_texts" in globals():
        _ru_journal_headers["_ru_journal_text(" + repr("{size=36}{u}Tuesday – Major Decisions{/u}{/size}") + ")"] = "_ru_journal_episode2_viewport"
    _ru_journal_wrapped = {}
    # Day 3 has two source vboxes, but only its left column has a heading.
    # The generated source-bound map identifies both exact locations and every
    # text descendant. Reuse the accepted left/right viewport geometries.
    _ru_journal_episode3_columns = {}
    if "_ru_episode3_journal_texts" in globals():
        if (set(_ru_episode3_journal_columns) != {("game/screens.rpy", 1208), ("game/screens.rpy", 1303)}
                or tuple(len(_ru_episode3_journal_columns[key]) for key in sorted(_ru_episode3_journal_columns)) != (27, 17)):
            raise Exception("Russian Episode 3 journal column scope changed")
        for _ru_column_location, _ru_column_sources in _ru_episode3_journal_columns.items():
            _ru_journal_episode3_columns[_ru_column_location] = (
                "_ru_journal_episode1_viewport" if _ru_column_location[1] == 1208 else "_ru_journal_episode2_viewport",
                {"_ru_journal_text(" + repr(source) + ")" for source in _ru_column_sources})
    # Extend the same source-bound column map for day 4. Historical internal
    # variable names stay unchanged so previous wrapping logic is identical.
    if "_ru_episode4_journal_texts" in globals():
        if (set(_ru_episode4_journal_columns) != {("game/screens.rpy", 1374), ("game/screens.rpy", 1461)}
                or tuple(len(_ru_episode4_journal_columns[key]) for key in sorted(_ru_episode4_journal_columns)) != (26, 46)):
            raise Exception("Russian Episode 4 journal column scope changed")
        if set(_ru_episode4_journal_columns).intersection(_ru_journal_episode3_columns):
            raise Exception("Russian journal column location collision")
        for _ru_column_location, _ru_column_sources in _ru_episode4_journal_columns.items():
            _ru_journal_episode3_columns[_ru_column_location] = (
                "_ru_journal_episode1_viewport" if _ru_column_location[1] == 1374 else "_ru_journal_episode2_viewport",
                {"_ru_journal_text(" + repr(source) + ")" for source in _ru_column_sources})
    _ru_journal_episode3_wrapped = {}
    _ru_journal_layout_texts = 0

    def _ru_journal_flow_text(node):
        global _ru_journal_layout_texts
        if isinstance(node, renpy.sl2.slast.SLDisplayable) and any(
                expr.startswith("_ru_journal_text(") for expr in node.positional):
            node.keyword = [(key, "0" if key in ("xpos", "ypos") else value)
                            for key, value in node.keyword]
            _ru_journal_layout_texts += 1
        for child in getattr(node, "children", ()):
            _ru_journal_flow_text(child)
        for _condition, block in getattr(node, "entries", ()):
            _ru_journal_flow_text(block)

    def _ru_journal_column_texts(node):
        found = []
        if isinstance(node, renpy.sl2.slast.SLDisplayable):
            found.extend(expr for expr in node.positional if expr.startswith("_ru_journal_text("))
        for child in getattr(node, "children", ()):
            found.extend(_ru_journal_column_texts(child))
        for _condition, block in getattr(node, "entries", ()):
            found.extend(_ru_journal_column_texts(block))
        return found

    def _ru_journal_wrap_episode(node):
        for index, child in enumerate(getattr(node, "children", ())):
            column_location = getattr(child, "location", None)
            episode3_column = _ru_journal_episode3_columns.get(column_location)
            headers = [header for header in _ru_journal_headers
                       if any(isinstance(item, renpy.sl2.slast.SLDisplayable)
                              and header in item.positional
                              for item in getattr(child, "children", ()))]
            if headers or episode3_column:
                if headers and len(headers) != 1:
                    raise Exception("Russian journal contains ambiguous page headers")
                if episode3_column:
                    column_texts = _ru_journal_column_texts(child)
                    if (headers or not isinstance(child, renpy.sl2.slast.SLDisplayable)
                            or getattr(child, "name", None) != "vbox"
                            or child.keyword != [("spacing", "10"), ("xmaximum", "550")]
                            or len(column_texts) != len(episode3_column[1])
                            or set(column_texts) != episode3_column[1]):
                        raise Exception("Russian Episode 3 journal column differs from the supported source")
                    template_name = episode3_column[0]
                else:
                    template_name = _ru_journal_headers[headers[0]]
                template = renpy.display.screen.screens[(template_name, None)].function
                if len(template.children) != 1:
                    raise Exception("Russian journal viewport template changed")
                viewport = _ru_journal_copy.deepcopy(template.children[0])
                viewport.displayable = _ru_journal_sl2viewport
                _ru_journal_flow_text(child)
                viewport.children = [child]
                node.children[index] = viewport
                if episode3_column:
                    _ru_journal_episode3_wrapped[column_location] = _ru_journal_episode3_wrapped.get(column_location, 0) + 1
                else:
                    header = headers[0]
                    _ru_journal_wrapped[header] = _ru_journal_wrapped.get(header, 0) + 1
            else:
                _ru_journal_wrap_episode(child)
        for _condition, block in getattr(node, "entries", ()):
            _ru_journal_wrap_episode(block)

    _ru_journal_wrap_episode(_ru_journal_screen)
    if (set(_ru_journal_wrapped) != set(_ru_journal_headers)
            or any(count != 1 for count in _ru_journal_wrapped.values())
            or set(_ru_journal_episode3_wrapped) != set(_ru_journal_episode3_columns)
            or any(count != 1 for count in _ru_journal_episode3_wrapped.values())
            or _ru_journal_layout_texts != len(_ru_journal_texts)):
        raise Exception("Russian journal page layout differs from the supported source")
    _ru_journal_screen.variant = repr("ru_pilot")
    _ru_journal_screen.location = ("game/zz_ru_accessibility.rpy", 1)
    _ru_journal_screen.const_ast = None
    _ru_journal_screen.not_const_ast = None
    _ru_journal_screen.analysis = None
    _ru_journal_screen.prepared = False
    _ru_journal_screen.define(_ru_journal_screen.location)

init 961 python:
    # This source screen combines vbox flow with increasing child ypos values.
    # At the original size35, Spectral measures55px high versus Kelmscott43px.
    # Compensate that12px difference between rows, retaining every text node,
    # original position expression and font size. The English SL2 tree stays intact.
    _ru_credits_original = renpy.display.screen.screens[("credits_6", None)]
    if not isinstance(_ru_credits_original.function, renpy.sl2.slast.SLScreen):
        raise Exception("Russian credits require the supported native SL2 screen")
    _ru_credits_screen = _ru_journal_copy.deepcopy(_ru_credits_original.function)
    _ru_credits_rows_y = tuple(range(150, 371, 20)) + (410, 430)
    _ru_credits_columns = []
    for _ru_credits_node in _ru_credits_screen.children:
        _ru_credits_children = getattr(_ru_credits_node, "children", ())
        if len(_ru_credits_children) != 14:
            continue
        if all(isinstance(child, renpy.sl2.slast.SLDisplayable)
               and dict(child.keyword).get("ypos") == str(y)
               and dict(child.keyword).get("xpos") == "960"
               and dict(child.keyword).get("text_align") == "0.5"
               for child, y in zip(_ru_credits_children, _ru_credits_rows_y)):
            _ru_credits_columns.append(_ru_credits_node)
    if len(_ru_credits_columns) != 1 or any(
            key == "spacing" for key, value in _ru_credits_columns[0].keyword):
        raise Exception("Russian credits column differs from the supported source")
    _ru_credits_columns[0].keyword.append(("spacing", "-12"))
    _ru_credits_screen.variant = repr("ru_pilot")
    _ru_credits_screen.location = ("game/zz_ru_accessibility.rpy", 182)
    _ru_credits_screen.const_ast = None
    _ru_credits_screen.not_const_ast = None
    _ru_credits_screen.analysis = None
    _ru_credits_screen.prepared = False
    _ru_credits_screen.define(_ru_credits_screen.location)
