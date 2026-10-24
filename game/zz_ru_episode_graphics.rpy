# Source artwork remains the base canvas. Only reviewed lettering regions are
# replaced with unmodified ImageGen raster crops, before scene transitions.

init 970 python:
    import json as _ru_episode_graphics_json
    import builtins as _ru_episode_graphics_builtin
    with renpy.file("ru_support/episode1_graphics.json") as _ru_episode_graphics_file:
        _ru_episode_graphics_data = _ru_episode_graphics_json.load(_ru_episode_graphics_file)
    if _ru_episode_graphics_data.get("schema_version") != 1:
        raise Exception("Russian episode graphics manifest version is unsupported")
    _ru_episode_graphic_specs = dict(_ru_episode_graphics_data["specs"])
    _ru_episode2_graphic_sources = _ru_episode_graphics_builtin.frozenset()
    # Older cumulative packages have no second-episode manifest. When present,
    # extend the source-bound registry before constructing any displayables.
    # An overlap is an error: accepted first-episode resources remain exact.
    if renpy.loadable("ru_support/episode2_graphics.json"):
        with renpy.file("ru_support/episode2_graphics.json") as _ru_episode_graphics_file:
            _ru_episode2_graphics_data = _ru_episode_graphics_json.load(_ru_episode_graphics_file)
        if (_ru_episode2_graphics_data.get("schema_version") != 1
                or _ru_episode2_graphics_data.get("source_archive_sha256") != "1dd82e3806b3be15cd209ad5ba955ea03a996519b69f8966d379b2a86205531c"
                or not isinstance(_ru_episode2_graphics_data.get("specs"), _ru_episode_graphics_builtin.dict)):
            raise Exception("Russian episode2 graphics manifest provenance is unsupported")
        if set(_ru_episode_graphic_specs).intersection(_ru_episode2_graphics_data["specs"]):
            raise Exception("Russian episode2 graphics override an accepted episode1 source")
        _ru_episode_graphic_specs.update(_ru_episode2_graphics_data["specs"])
        _ru_episode2_graphic_sources = _ru_episode_graphics_builtin.frozenset(_ru_episode2_graphics_data["specs"])
    _ru_episode3_graphic_sources = _ru_episode_graphics_builtin.frozenset()
    if renpy.loadable("ru_support/episode3_graphics.json"):
        with renpy.file("ru_support/episode3_graphics.json") as _ru_episode_graphics_file:
            _ru_episode3_graphics_data = _ru_episode_graphics_json.load(_ru_episode_graphics_file)
        if (_ru_episode3_graphics_data.get("schema_version") != 1
                or _ru_episode3_graphics_data.get("source_archive_sha256") != "1dd82e3806b3be15cd209ad5ba955ea03a996519b69f8966d379b2a86205531c"
                or not isinstance(_ru_episode3_graphics_data.get("specs"), _ru_episode_graphics_builtin.dict)):
            raise Exception("Russian episode3 graphics manifest provenance is unsupported")
        if set(_ru_episode_graphic_specs).intersection(_ru_episode3_graphics_data["specs"]):
            raise Exception("Russian episode3 graphics override an accepted earlier source")
        _ru_episode_graphic_specs.update(_ru_episode3_graphics_data["specs"])
        _ru_episode3_graphic_sources = _ru_episode_graphics_builtin.frozenset(_ru_episode3_graphics_data["specs"])
    _ru_episode4_graphic_sources = _ru_episode_graphics_builtin.frozenset()
    if renpy.loadable("ru_support/episode4_graphics.json"):
        with renpy.file("ru_support/episode4_graphics.json") as _ru_episode_graphics_file:
            _ru_episode4_graphics_data = _ru_episode_graphics_json.load(_ru_episode_graphics_file)
        if (_ru_episode4_graphics_data.get("schema_version") != 1
                or _ru_episode4_graphics_data.get("source_archive_sha256") != "1dd82e3806b3be15cd209ad5ba955ea03a996519b69f8966d379b2a86205531c"
                or not isinstance(_ru_episode4_graphics_data.get("specs"), _ru_episode_graphics_builtin.dict)):
            raise Exception("Russian episode4 graphics manifest provenance is unsupported")
        if set(_ru_episode_graphic_specs).intersection(_ru_episode4_graphics_data["specs"]):
            raise Exception("Russian episode4 graphics override an accepted earlier source")
        _ru_episode_graphic_specs.update(_ru_episode4_graphics_data["specs"])
        _ru_episode4_graphic_sources = _ru_episode_graphics_builtin.frozenset(_ru_episode4_graphics_data["specs"])
    _ru_episode5_graphic_sources = _ru_episode_graphics_builtin.frozenset()
    if renpy.loadable("ru_support/episode5_graphics.json"):
        with renpy.file("ru_support/episode5_graphics.json") as _ru_episode_graphics_file:
            _ru_episode5_graphics_data = _ru_episode_graphics_json.load(_ru_episode_graphics_file)
        if (_ru_episode5_graphics_data.get("schema_version") != 1
                or _ru_episode5_graphics_data.get("source_archive_sha256") != "1dd82e3806b3be15cd209ad5ba955ea03a996519b69f8966d379b2a86205531c"
                or not isinstance(_ru_episode5_graphics_data.get("specs"), _ru_episode_graphics_builtin.dict)):
            raise Exception("Russian episode5 graphics manifest provenance is unsupported")
        if set(_ru_episode_graphic_specs).intersection(_ru_episode5_graphics_data["specs"]):
            raise Exception("Russian episode5 graphics override an accepted earlier source")
        _ru_episode_graphic_specs.update(_ru_episode5_graphics_data["specs"])
        _ru_episode5_graphic_sources = _ru_episode_graphics_builtin.frozenset(_ru_episode5_graphics_data["specs"])
    _ru_episode_graphic_cache = {}

    def _ru_episode_check_rect(rect, size):
        left, top, right, bottom = rect
        width, height = size
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise Exception("Russian episode graphic has invalid region bounds")

    class _RuEpisodePolygonMask(renpy.Displayable):
        # A geometric alpha mask only. All visible lettering comes from the
        # unmodified generated raster. No font or painted content is produced.
        # Render.canvas API: https://www.renpy.org/doc/html/cdd.html
        def __init__(self, size, points, **properties):
            super(_RuEpisodePolygonMask, self).__init__(**properties)
            self.mask_size = tuple(size)
            self.points = tuple(tuple(point) for point in points)
            if len(self.points) < 3 or any(not (0 <= x < size[0] and 0 <= y < size[1])
                                           for x, y in self.points):
                raise Exception("Russian episode graphic has an invalid polygon mask")

        def render(self, width, height, st, at):
            result = renpy.Render(*self.mask_size)
            result.canvas().polygon((255, 255, 255, 255), self.points, 0)
            return result

    class _RuEpisodeSourceKeepMask(renpy.Displayable):
        # Binary geometry only: preserve the original alpha exactly outside
        # approved lettering rectangles, clear it inside for transparent ink.
        def __init__(self, size, rectangles, polygons=(), **properties):
            super(_RuEpisodeSourceKeepMask, self).__init__(**properties)
            self.mask_size = tuple(size)
            self.rectangles = tuple(tuple(rect) for rect in rectangles)
            self.polygons = tuple(tuple(tuple(point) for point in points) for points in polygons)
            for rect in self.rectangles:
                _ru_episode_check_rect(rect, self.mask_size)
            for points in self.polygons:
                if len(points) < 3 or any(not (0 <= x < size[0] and 0 <= y < size[1]) for x, y in points):
                    raise Exception("Russian episode graphic has an invalid clearing polygon")

        def render(self, width, height, st, at):
            result = renpy.Render(*self.mask_size)
            # Each Render.canvas() call creates another composited surface.
            # Clear polygons on the SAME surface that was filled opaque.
            canvas = result.canvas()
            surface = canvas.get_surface()
            surface.fill((255, 255, 255, 255))
            for left, top, right, bottom in self.rectangles:
                surface.fill((0, 0, 0, 0), (left, top, right - left, bottom - top))
            for points in self.polygons:
                canvas.polygon((0, 0, 0, 0), points, 0)
            return result

    class _RuEpisodeNativeBaseAlphaMask(AlphaMask):
        # Preserve the original canvas before the final screen scaling. GL2's
        # drawable-resolution FBO rounds 1040 * 2/3 to 693, then scales again.
        def render(self, width, height, st, at):
            result = super(_RuEpisodeNativeBaseAlphaMask, self).render(width, height, st, at)
            result.add_property("drawable_resolution", False)
            return result

    def ru_episode_graphic(source):
        if source in _ru_episode_graphic_cache:
            return _ru_episode_graphic_cache[source]
        spec = _ru_episode_graphic_specs[source]
        if not renpy.loadable(source) or not renpy.loadable(spec["artifact"]):
            raise Exception("Russian episode graphic source or raster is missing")
        base = Image(source)
        clears = list(spec.get("source_clear_rects", ()))
        clear_polygons = []
        for region in spec["regions"]:
            if region.get("replace_original_alpha"):
                if region.get("mask_feather_sigma") or region.get("original_alpha_clip"):
                    raise Exception("Original alpha replacement requires one binary mask")
                if "destination_clip_polygon" in region:
                    clear_polygons.append(region["destination_clip_polygon"])
                else:
                    clears.append(region["destination_rect"])
        # New E2/E3 clear/refill layers resolve together at source resolution.
        # Keep the accepted E1 branch and English Image object unchanged.
        native_compose = bool(clears or clear_polygons) and (
            tuple(spec["source_size"]) == (1920, 1040)
            or source in _ru_episode2_graphic_sources or source in _ru_episode3_graphic_sources
            or source in _ru_episode4_graphic_sources or source in _ru_episode5_graphic_sources)
        alpha_mask = _RuEpisodeNativeBaseAlphaMask if native_compose else AlphaMask
        if native_compose:
            # A private neutral Render prevents RTT cache writes on the shared Image Render.
            base = Transform(base)
        if clears or clear_polygons:
            base = alpha_mask(base, _RuEpisodeSourceKeepMask(spec["source_size"], clears, clear_polygons))
        layers = [(0, 0), base]
        for region in spec["regions"]:
            generated, destination = region["generated_rect"], region["destination_rect"]
            _ru_episode_check_rect(generated, spec["artifact_size"])
            _ru_episode_check_rect(destination, spec["source_size"])
            left, top, right, bottom = generated
            x, y, end_x, end_y = destination
            raster = spec["artifact"]
            if region.get("replace_original_alpha"):
                # Operate on straight RGB before GPU premultiplication, then
                # apply source alpha exactly once to the replacement region.
                raster = im.MatrixColor(raster, im.matrix([
                    1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0, 0, 0, 0, 0, 1]))
            crop = Crop((left, top, right - left, bottom - top), raster)
            part = Transform(crop, xsize=end_x - x, ysize=end_y - y)
            for fit in (spec.get("colour_fit"), region.get("colour_fit")):
                if fit is None:
                    continue
                (rs, ro), (gs, go), (bs, bo) = fit
                # Fits use original 0..255 source channel values; Ren'Py's
                # premultiplied colour matrix uses normalized channel offsets.
                part = Transform(part, matrixcolor=Matrix([
                    rs, 0, 0, ro / 255.0, 0, gs, 0, go / 255.0,
                    0, 0, bs, bo / 255.0, 0, 0, 0, 1]))
            if "alpha_scale" in region:
                if not 0 < region["alpha_scale"] <= 1:
                    raise Exception("Russian episode ink opacity is outside its bounds")
                part = Transform(part, alpha=region["alpha_scale"])
            if region.get("original_alpha_clip") or region.get("replace_original_alpha"):
                part = alpha_mask(part, Crop((x, y, end_x - x, end_y - y), Image(source)))
            if "destination_clip_polygon" in region:
                points = [(px - x, py - y) for px, py in region["destination_clip_polygon"]]
                mask = _RuEpisodePolygonMask((end_x - x, end_y - y), points)
                feather = region.get("mask_feather_sigma", 0)
                if feather:
                    # Smooth only the geometric edge. The generated lettering
                    # itself is never blurred or redrawn.
                    if not 0 < feather <= 2:
                        raise Exception("Russian episode graphic mask feather is outside its bounds")
                    if native_compose:
                        mask = Transform(mask, blur=feather, gl_drawable_resolution=False)
                    else:
                        mask = Transform(mask, blur=feather)
                part = alpha_mask(part, mask)
            if "destination_exclude_polygons" in region:
                # Binary holes preserve the source foreground exactly. Apply
                # after feathering the outer edge so it cannot bleed into
                # original folds, hands or other foreground artwork.
                exclusions = region["destination_exclude_polygons"]
                if (region.get("replace_original_alpha") or not 1 <= len(exclusions) <= 64
                        or any(not 3 <= len(points) <= 128 for points in exclusions)):
                    raise Exception("Russian episode foreground exclusions are invalid")
                local = []
                for points in exclusions:
                    if any(type(px) is not int or type(py) is not int
                           or not (x <= px < end_x and y <= py < end_y) for px, py in points):
                        raise Exception("Russian episode foreground exclusion is out of bounds")
                    pl, pt = min(p[0] for p in points), min(p[1] for p in points)
                    pr, pb = max(p[0] for p in points) + 1, max(p[1] for p in points) + 1
                    if any(max(pl, cl) < min(pr, cr) and max(pt, ct) < min(pb, cb)
                           for cl, ct, cr, cb in clears):
                        raise Exception("Russian episode foreground exclusion overlaps source clearing")
                    if any(other is not region
                           and max(pl, other["destination_rect"][0]) < min(pr, other["destination_rect"][2])
                           and max(pt, other["destination_rect"][1]) < min(pb, other["destination_rect"][3])
                           for other in spec["regions"]):
                        raise Exception("Russian episode foreground exclusion overlaps another replacement")
                    local.append([(px - x, py - y) for px, py in points])
                part = alpha_mask(part, _RuEpisodeSourceKeepMask(
                    (end_x - x, end_y - y), (), local))
            layers.extend(((x, y), part))
        result = Composite(tuple(spec["source_size"]), *layers)
        if native_compose:
            # Resolve binary clear/refill together before any final screen resampling.
            result = Flatten(result, drawable_resolution=False)
        _ru_episode_graphic_cache[source] = result
        return result

    for _ru_e1_source, _ru_e1_spec in _ru_episode_graphic_specs.items():
        for _ru_e1_name in _ru_e1_spec["image_names"]:
            _ru_e1_original = renpy.get_registered_image(_ru_e1_name)
            if _ru_e1_original is None:
                raise Exception("Russian episode graphic image registration is missing: " + _ru_e1_name)
            if getattr(_ru_e1_original, "filename", None) != _ru_e1_source:
                raise Exception("Russian episode graphic does not match the registered source: " + _ru_e1_name)
            # Preserve the registered English object verbatim, including its
            # identity and all engine-owned prediction/placement behavior.
            renpy.image(_ru_e1_name, DynamicDisplayable(_ru_language_graphic,
                ru_episode_graphic(_ru_e1_source), _ru_e1_original))
