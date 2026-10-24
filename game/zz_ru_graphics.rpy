# Original source canvases remain intact outside finite lettering regions.
# Accepted ImageGen raster bytes are reused without creating new artwork.

init 950 python:
    import json as _ru_pilot_graphics_json
    import math as _ru_pilot_graphics_math
    with renpy.file("ru_support/pilot_graphics_regions.json") as _ru_pilot_graphics_file:
        _ru_pilot_graphics_data = _ru_pilot_graphics_json.load(_ru_pilot_graphics_file)
    if _ru_pilot_graphics_data.get("schema_version") != 1:
        raise Exception("Russian pilot graphics manifest version is unsupported")
    _ru_graphic_specs = _ru_pilot_graphics_data["specs"]
    _ru_pilot_auxiliary = _ru_pilot_graphics_data.get("auxiliary_rasters", {})
    _ru_graphic_original_only = {entry["source"]: entry
        for entry in _ru_pilot_graphics_data["original_only"]}
    _ru_graphic_cache = {}

    # Re-sample only a generated cleanplate, never the original source image.
    # Pixel-centre conversion matches the numerical source-neighbour fit.
    renpy.register_shader("ru.pilot_plate_uv", variables="""
        uniform sampler2D tex0;
        varying vec2 v_tex_coord;
        uniform vec4 u_ru_plate_h0;
        uniform vec4 u_ru_plate_h1;
        uniform vec2 u_ru_plate_dest_size;
        uniform vec2 u_ru_plate_tex_size;
    """, fragment_300="""
        vec2 uv = (v_tex_coord * u_ru_plate_dest_size - vec2(0.5)) / (u_ru_plate_dest_size - vec2(1.0));
        float denom = u_ru_plate_h0.w * uv.x + u_ru_plate_h1.w * uv.y + 1.0;
        vec2 mapped = vec2(dot(u_ru_plate_h0.xyz, vec3(uv, 1.0)), dot(u_ru_plate_h1.xyz, vec3(uv, 1.0))) / denom;
        vec2 sample_uv = (clamp(mapped, 0.0, 1.0) * (u_ru_plate_tex_size - vec2(1.0)) + vec2(0.5)) / u_ru_plate_tex_size;
        gl_FragColor = texture2D(tex0, sample_uv);
    """)

    def _ru_pilot_check_rect(rect, size):
        if len(rect) != 4 or any(type(value) is not int for value in rect):
            raise Exception("Russian pilot graphic region is not an integer rectangle")
        left, top, right, bottom = rect
        width, height = size
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise Exception("Russian pilot graphic has invalid region bounds")

    class _RuPilotKeepArtworkMask(renpy.Displayable):
        # Binary geometry only; holes protect the actual original drawing.
        def __init__(self, size, protected, feather=0, **properties):
            super(_RuPilotKeepArtworkMask, self).__init__(**properties)
            self.mask_size = tuple(size)
            self.protected = tuple(tuple(tuple(point) for point in points)
                                   for points in protected)
            self.feather = feather

        def render(self, width, height, st, at):
            result = renpy.Render(*self.mask_size)
            canvas = result.canvas()
            canvas.get_surface().fill((255, 255, 255, 255))
            if self.feather:
                surface = canvas.get_surface()
                surface.fill((0, 0, 0, 0))
                for inset in range(self.feather):
                    alpha = int(255 * inset / self.feather)
                    surface.fill((255, 255, 255, alpha),
                                 (inset, inset, self.mask_size[0]-2*inset, self.mask_size[1]-2*inset))
                inset = self.feather
                surface.fill((255, 255, 255, 255),
                             (inset, inset, self.mask_size[0]-2*inset, self.mask_size[1]-2*inset))
            for points in self.protected:
                canvas.polygon((0, 0, 0, 0), points, 0)
            return result

    class _RuPilotNativeBaseAlphaMask(AlphaMask):
        # Resolve source clearing at original pixel size. A drawable-resolution
        # FBO would round the native canvas at 720p and then resample it again.
        def render(self, width, height, st, at):
            result = super(_RuPilotNativeBaseAlphaMask, self).render(width, height, st, at)
            result.add_property("drawable_resolution", False)
            return result

    def _ru_validate_graphic_spec(source, spec):
        if not (source.startswith("gui/") or source ==
                "images/_episode 1/_bg/monday_woods_climax/bg hardcore warning.png"):
            raise Exception("Russian pilot graphic source is outside its finite family")
        if not spec["artifact"].startswith("ru_support/images/"):
            raise Exception("Russian pilot graphic artifact is outside its support directory")
        if len(spec["regions"]) not in (1, 2, 4):
            raise Exception("Russian pilot graphic has an unexpected number of lettering regions")
        for size_key in ("source_size", "artifact_size"):
            size = spec[size_key]
            if len(size) != 2 or any(type(value) is not int or not 1 <= value <= 4096 for value in size):
                raise Exception("Russian pilot graphic has invalid canvas dimensions")
        width, height = spec["source_size"]
        for points in spec["protected_polygons"]:
            if not 3 <= len(points) <= 32 or any(type(x) is not int or type(y) is not int
                    or not (0 <= x < width and 0 <= y < height) for x, y in points):
                raise Exception("Russian pilot graphic has an invalid artwork guard")
        for region in spec["regions"]:
            _ru_pilot_check_rect(region["generated_rect"], spec["artifact_size"])
            _ru_pilot_check_rect(region["destination_rect"], spec["source_size"])
            x, y, right, bottom = region["destination_rect"]
            if (right - x) * (bottom - y) >= width * height * 0.7:
                raise Exception("Russian pilot lettering region covers too much of its source")
            feather = region.get("edge_feather", 0)
            if (type(feather) is not int or not 0 <= feather <= 5
                    or 2 * feather >= min(right - x, bottom - y)):
                raise Exception("Russian pilot graphic has invalid finite feather bounds")
            for colour_key, count in (("background_rgb", 3), ("background_rgba", 4)):
                if colour_key in region:
                    colour = region[colour_key]
                    if len(colour) != count or any(type(value) is not int or not 0 <= value <= 255
                                                  for value in colour):
                        raise Exception("Russian pilot graphic has invalid background channels")
            if "background_sample_rect" in region:
                _ru_pilot_check_rect(region["background_sample_rect"], spec["source_size"])
            if sum(key in region for key in ("background_rgb", "background_rgba", "background_sample_rect")) > 1:
                raise Exception("Russian pilot graphic has conflicting background methods")
            if "ink_extract" in region:
                ink = region["ink_extract"]
                if (type(ink["channel"]) is not int or ink["channel"] not in (0, 1, 2)
                        or type(ink["opaque"]) is not int or type(ink["clear"]) is not int
                        or not 0 <= ink["opaque"] < ink["clear"] <= 255
                        or len(ink["rgb"]) != 3 or any(type(value) is not int or not 0 <= value <= 255
                                                       for value in ink["rgb"])):
                    raise Exception("Russian pilot graphic has invalid raster ink extraction")
            if "colour_fit" in region:
                fit = region["colour_fit"]
                if (len(fit) != 3 or any(len(pair) != 2 for pair in fit)
                        or any(type(value) not in (int, float) or not _ru_pilot_graphics_math.isfinite(value)
                               for pair in fit for value in pair)
                        or any(not 0 < scale <= 4 or not -255 <= offset <= 255 for scale, offset in fit)):
                    raise Exception("Russian pilot graphic has invalid finite colour correction")
            if "tint" in region:
                tint = region["tint"]
                if (type(tint) is not str or len(tint) != 7 or tint[0] != "#"
                        or any(value not in "0123456789abcdefABCDEF" for value in tint[1:])):
                    raise Exception("Russian pilot graphic has invalid tint channels")
            if "replace_original_alpha" in region:
                if (type(region["replace_original_alpha"]) is not bool
                        or region["replace_original_alpha"] and (feather or spec["protected_polygons"])):
                    raise Exception("Russian pilot alpha replacement conflicts with finite masks")
            if ("letter_mask" in region) != ("background_repair" in region):
                raise Exception("Russian pilot glyph masks require one bounded background repair")
            if "background_repair" in region:
                repair=region["background_repair"]
                for path,role in ((region["letter_mask"],"generated_letter_mask"),
                        (repair["artifact"],"generated_background_cleanplate"),
                        (repair["source_erase_mask"],"original_english_mask")):
                    if path not in _ru_pilot_auxiliary or _ru_pilot_auxiliary[path]["role"] != role:
                        raise Exception("Russian pilot glyph repair has an unregistered auxiliary raster")
                if (_ru_pilot_auxiliary[region["letter_mask"]]["size"] != spec["artifact_size"]
                        or min(right-x,bottom-y)<2
                        or feather or region.get("replace_original_alpha") or "ink_extract" in region):
                    raise Exception("Russian pilot glyph geometry conflicts with another replacement method")
                _ru_pilot_check_rect(repair["generated_rect"],_ru_pilot_auxiliary[repair["artifact"]]["size"])
                _ru_pilot_check_rect(repair["source_mask_rect"],_ru_pilot_auxiliary[repair["source_erase_mask"]]["size"])
                h=repair["uv_homography"]
                identity=(1,0,0,0,1,0,0,0); limits=(.35,.35,.2,.35,.35,.2,.3,.3)
                if (len(h)!=8 or any(type(v) not in (int,float) or not _ru_pilot_graphics_math.isfinite(v) for v in h)
                        or any(abs(v-i)>limit for v,i,limit in zip(h,identity,limits))):
                    raise Exception("Russian pilot background registration is outside finite bounds")
                a,b,c,d,e,f,g,hh=h
                determinant=a*(e-f*hh)-b*(d-f*g)+c*(d*hh-e*g)
                if not .1 <= abs(determinant) <= 4 or any(g*u+hh*v+1<.4 for u in (0,1) for v in (0,1)):
                    raise Exception("Russian pilot background registration is degenerate")
                fit=repair["colour_fit"]
                if (len(fit)!=3 or any(len(pair)!=2 for pair in fit)
                        or any(type(v) not in (int,float) or not _ru_pilot_graphics_math.isfinite(v) for pair in fit for v in pair)
                        or any(not 0<s<=4 or not -255<=o<=255 for s,o in fit)):
                    raise Exception("Russian pilot background colour fit is outside finite bounds")

    for _ru_aux_path, _ru_aux_meta in _ru_pilot_auxiliary.items():
        if (not _ru_aux_path.startswith("ru_support/images/pilot_refresh/") or ".." in _ru_aux_path
                or _ru_aux_meta["role"] not in ("original_english_mask","generated_letter_mask","generated_background_cleanplate")
                or len(_ru_aux_meta["size"])!=2 or any(type(v) is not int or not 1<=v<=4096 for v in _ru_aux_meta["size"])
                or not renpy.loadable(_ru_aux_path)):
            raise Exception("Russian pilot auxiliary raster metadata is invalid")

    for _ru_graphic_source, _ru_graphic_spec in _ru_graphic_specs.items():
        _ru_validate_graphic_spec(_ru_graphic_source, _ru_graphic_spec)

    def _ru_normalized_graphic(source, spec):
        if not renpy.loadable(source) or not renpy.loadable(spec["artifact"]):
            raise Exception("Russian pilot graphic source or lettering raster is missing")
        base=Image(source)
        clears=[]
        for region in spec["regions"]:
            if region.get("replace_original_alpha"):
                l,t,r,b=region["destination_rect"]
                clears.append([(l,t),(r-1,t),(r-1,b-1),(l,b-1)])
        if clears:
            # Keep RTT properties off the shared original Image Render, which
            # also supplies unchanged English and other source-state paths.
            base=Transform(base)
            base=_RuPilotNativeBaseAlphaMask(base,_RuPilotKeepArtworkMask(spec["source_size"],clears))
        layers = [(0, 0), base]
        for region in spec["regions"]:
            left, top, right, bottom = region["generated_rect"]
            x, y, end_x, end_y = region["destination_rect"]
            # Accepted lettering and its bounded background restoration only.
            # All remaining pixels come from this exact original source state.
            raster = spec["artifact"]
            if "ink_extract" in region:
                ink = region["ink_extract"]
                scale = 255.0 / (ink["clear"] - ink["opaque"])
                alpha = [0, 0, 0, 0, ink["clear"] / (ink["clear"] - ink["opaque"])]
                alpha[ink["channel"]] = -scale
                red, green, blue = [value/255.0 for value in ink["rgb"]]
                raster = im.MatrixColor(raster, im.matrix([
                    0, 0, 0, 0, red, 0, 0, 0, 0, green, 0, 0, 0, 0, blue] + alpha))
            part = Transform(Crop((left, top, right - left, bottom - top), raster),
                             xsize=end_x - x, ysize=end_y - y)
            if "background_rgb" in region:
                colour = "#%02x%02x%02x" % tuple(region["background_rgb"])
                part = Composite((end_x-x,end_y-y), (0,0), Solid(colour), (0,0), part)
            if "background_sample_rect" in region:
                bl,bt,br,bb=region["background_sample_rect"]
                background=Transform(Crop((bl,bt,br-bl,bb-bt),source),xsize=end_x-x,ysize=end_y-y)
                part=Composite((end_x-x,end_y-y),(0,0),background,(0,0),part)
            if "background_rgba" in region:
                colour="#%02x%02x%02x%02x" % tuple(region["background_rgba"])
                part=Composite((end_x-x,end_y-y),(0,0),Solid(colour),(0,0),part)
            if "colour_fit" in region:
                (rs, ro), (gs, go), (bs, bo) = region["colour_fit"]
                part = Transform(part, matrixcolor=Matrix([
                    rs, 0, 0, ro / 255.0, 0, gs, 0, go / 255.0,
                    0, 0, bs, bo / 255.0, 0, 0, 0, 1]))
            if "tint" in region:
                part = Transform(part, matrixcolor=TintMatrix(region["tint"]))
            if "background_repair" in region:
                repair=region["background_repair"]
                letter_mask=Transform(Crop((left,top,right-left,bottom-top),region["letter_mask"]),
                                      xsize=end_x-x,ysize=end_y-y)
                part=_RuPilotNativeBaseAlphaMask(Transform(part),letter_mask)
                pl,pt,pr,pb=repair["generated_rect"]
                a,b,c,d,e,f,g,h=repair["uv_homography"]
                background=Transform(Crop((pl,pt,pr-pl,pb-pt),repair["artifact"]),
                    xsize=end_x-x,ysize=end_y-y,mesh=True,shader="ru.pilot_plate_uv",gl_drawable_resolution=False,
                    u_ru_plate_h0=(a,b,c,g),u_ru_plate_h1=(d,e,f,h),
                    u_ru_plate_dest_size=(float(end_x-x),float(end_y-y)),u_ru_plate_tex_size=(float(pr-pl),float(pb-pt)))
                (rs,ro),(gs,go),(bs,bo)=repair["colour_fit"]
                background=Transform(background,matrixcolor=Matrix([
                    rs,0,0,ro/255.0,0,gs,0,go/255.0,0,0,bs,bo/255.0,0,0,0,1]))
                ml,mt,mr,mb=repair["source_mask_rect"]
                erase_mask=Transform(Crop((ml,mt,mr-ml,mb-mt),repair["source_erase_mask"]),
                                     xsize=end_x-x,ysize=end_y-y)
                background=_RuPilotNativeBaseAlphaMask(Transform(background),erase_mask)
                part=Composite((end_x-x,end_y-y),(0,0),background,(0,0),part)
            if spec["protected_polygons"] or region.get("edge_feather"):
                local = [[(px - x, py - y) for px, py in points]
                         for points in spec["protected_polygons"]]
                mask_class=_RuPilotNativeBaseAlphaMask if "background_repair" in region else AlphaMask
                part = mask_class(part, _RuPilotKeepArtworkMask((end_x - x, end_y - y), local,
                                 feather=region.get("edge_feather",0)))
            if "background_repair" in region:
                part=Flatten(part,drawable_resolution=False)
            layers.extend(((x, y), part))
        result=Composite(tuple(spec["source_size"]), *layers)
        if clears:
            # Only the five alpha230 paper fields use clear/refill. Resolve
            # their source and lettering together before final screen scaling.
            result=Flatten(result,drawable_resolution=False)
        return result

    def ru_graphic(source):
        """Resolve only the reviewed finite family in its actual source canvas."""
        if source not in _ru_graphic_cache:
            if source in _ru_graphic_specs:
                result = _ru_normalized_graphic(source, _ru_graphic_specs[source])
            elif source in _ru_graphic_original_only:
                result = Image(source)
            else:
                raise Exception("Russian graphic has no reviewed mapping: " + source)
            _ru_graphic_cache[source] = result
        return _ru_graphic_cache[source]

    def _ru_language_graphic(st, at, russian, original):
        return (russian if ru_is_active() else original), None

    def ru_register_graphic(name, source, **placement):
        """Choose language before the first transition frame; preserve English object."""
        original = renpy.get_registered_image(name)
        if original is None:
            raise Exception("Russian graphic image registration is missing: " + name)
        russian = ru_graphic(source)
        if placement:
            russian = Transform(russian, **placement)
        renpy.image(name, DynamicDisplayable(_ru_language_graphic, russian, original))

    # Original image statements run at init priority 500. Language dispatch is
    # available at initial placement/render, including the original fades.
    ru_register_graphic("c_name", "gui/textbox_character_name.png", yalign=0.5)
    ru_register_graphic("c_town", "gui/textbox_character_city.png", yalign=0.5)
    ru_register_graphic("bg hardcore warning", "images/_episode 1/_bg/monday_woods_climax/bg hardcore warning.png")
