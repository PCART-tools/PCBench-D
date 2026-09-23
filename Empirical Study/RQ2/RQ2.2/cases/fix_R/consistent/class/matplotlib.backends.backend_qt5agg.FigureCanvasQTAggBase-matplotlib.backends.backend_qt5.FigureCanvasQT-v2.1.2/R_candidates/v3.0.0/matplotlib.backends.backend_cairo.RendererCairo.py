class RendererCairo(RendererBase):
    fontweights = {
        100          : cairo.FONT_WEIGHT_NORMAL,
        200          : cairo.FONT_WEIGHT_NORMAL,
        300          : cairo.FONT_WEIGHT_NORMAL,
        400          : cairo.FONT_WEIGHT_NORMAL,
        500          : cairo.FONT_WEIGHT_NORMAL,
        600          : cairo.FONT_WEIGHT_BOLD,
        700          : cairo.FONT_WEIGHT_BOLD,
        800          : cairo.FONT_WEIGHT_BOLD,
        900          : cairo.FONT_WEIGHT_BOLD,
        'ultralight' : cairo.FONT_WEIGHT_NORMAL,
        'light'      : cairo.FONT_WEIGHT_NORMAL,
        'normal'     : cairo.FONT_WEIGHT_NORMAL,
        'medium'     : cairo.FONT_WEIGHT_NORMAL,
        'regular'    : cairo.FONT_WEIGHT_NORMAL,
        'semibold'   : cairo.FONT_WEIGHT_BOLD,
        'bold'       : cairo.FONT_WEIGHT_BOLD,
        'heavy'      : cairo.FONT_WEIGHT_BOLD,
        'ultrabold'  : cairo.FONT_WEIGHT_BOLD,
        'black'      : cairo.FONT_WEIGHT_BOLD,
                   }
    fontangles = {
        'italic'  : cairo.FONT_SLANT_ITALIC,
        'normal'  : cairo.FONT_SLANT_NORMAL,
        'oblique' : cairo.FONT_SLANT_OBLIQUE,
        }


    def __init__(self, dpi):
        self.dpi = dpi
        self.gc = GraphicsContextCairo(renderer=self)
        self.text_ctx = cairo.Context(
           cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
        self.mathtext_parser = MathTextParser('Cairo')
        RendererBase.__init__(self)

    def set_ctx_from_surface(self, surface):
        self.gc.ctx = cairo.Context(surface)
        # Although it may appear natural to automatically call
        # `self.set_width_height(surface.get_width(), surface.get_height())`
        # here (instead of having the caller do so separately), this would fail
        # for PDF/PS/SVG surfaces, which have no way to report their extents.

    def set_width_height(self, width, height):
        self.width  = width
        self.height = height

    def _fill_and_stroke(self, ctx, fill_c, alpha, alpha_overrides):
        if fill_c is not None:
            ctx.save()
            if len(fill_c) == 3 or alpha_overrides:
                ctx.set_source_rgba(fill_c[0], fill_c[1], fill_c[2], alpha)
            else:
                ctx.set_source_rgba(fill_c[0], fill_c[1], fill_c[2], fill_c[3])
            ctx.fill_preserve()
            ctx.restore()
        ctx.stroke()

    @staticmethod
    @cbook.deprecated("3.0")
    def convert_path(ctx, path, transform, clip=None):
        _append_path(ctx, path, transform, clip)

    def draw_path(self, gc, path, transform, rgbFace=None):
        ctx = gc.ctx
        # Clip the path to the actual rendering extents if it isn't filled.
        clip = (ctx.clip_extents()
                if rgbFace is None and gc.get_hatch() is None
                else None)
        transform = (transform
                     + Affine2D().scale(1, -1).translate(0, self.height))
        ctx.new_path()
        _append_path(ctx, path, transform, clip)
        self._fill_and_stroke(
            ctx, rgbFace, gc.get_alpha(), gc.get_forced_alpha())

    def draw_markers(self, gc, marker_path, marker_trans, path, transform,
                     rgbFace=None):
        ctx = gc.ctx

        ctx.new_path()
        # Create the path for the marker; it needs to be flipped here already!
        _append_path(ctx, marker_path, marker_trans + Affine2D().scale(1, -1))
        marker_path = ctx.copy_path_flat()

        # Figure out whether the path has a fill
        x1, y1, x2, y2 = ctx.fill_extents()
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
            filled = False
            # No fill, just unset this (so we don't try to fill it later on)
            rgbFace = None
        else:
            filled = True

        transform = (transform
                     + Affine2D().scale(1, -1).translate(0, self.height))

        ctx.new_path()
        for i, (vertices, codes) in enumerate(
                path.iter_segments(transform, simplify=False)):
            if len(vertices):
                x, y = vertices[-2:]
                ctx.save()

                # Translate and apply path
                ctx.translate(x, y)
                ctx.append_path(marker_path)

                ctx.restore()

                # Slower code path if there is a fill; we need to draw
                # the fill and stroke for each marker at the same time.
                # Also flush out the drawing every once in a while to
                # prevent the paths from getting way too long.
                if filled or i % 1000 == 0:
                    self._fill_and_stroke(
                        ctx, rgbFace, gc.get_alpha(), gc.get_forced_alpha())

        # Fast path, if there is no fill, draw everything in one step
        if not filled:
            self._fill_and_stroke(
                ctx, rgbFace, gc.get_alpha(), gc.get_forced_alpha())

    def draw_path_collection(
            self, gc, master_transform, paths, all_transforms, offsets,
            offsetTrans, facecolors, edgecolors, linewidths, linestyles,
            antialiaseds, urls, offset_position):

        path_ids = []
        for path, transform in self._iter_collection_raw_paths(
                master_transform, paths, all_transforms):
            path_ids.append((path, Affine2D(transform)))

        reuse_key = None
        grouped_draw = []

        def _draw_paths():
            if not grouped_draw:
                return
            gc_vars, rgb_fc = reuse_key
            gc = copy.copy(gc0)
            # We actually need to call the setters to reset the internal state.
            vars(gc).update(gc_vars)
            for k, v in gc_vars.items():
                if k == "_linestyle":  # Deprecated, no effect.
                    continue
                try:
                    getattr(gc, "set" + k)(v)
                except (AttributeError, TypeError) as e:
                    pass
            gc.ctx.new_path()
            paths, transforms = zip(*grouped_draw)
            grouped_draw.clear()
            _append_paths(gc.ctx, paths, transforms)
            self._fill_and_stroke(
                gc.ctx, rgb_fc, gc.get_alpha(), gc.get_forced_alpha())

        for xo, yo, path_id, gc0, rgb_fc in self._iter_collection(
                gc, master_transform, all_transforms, path_ids, offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):
            path, transform = path_id
            transform = (Affine2D(transform.get_matrix())
                         .translate(xo, yo - self.height).scale(1, -1))
            # rgb_fc could be a ndarray, for which equality is elementwise.
            new_key = vars(gc0), tuple(rgb_fc) if rgb_fc is not None else None
            if new_key == reuse_key:
                grouped_draw.append((path, transform))
            else:
                _draw_paths()
                grouped_draw.append((path, transform))
                reuse_key = new_key
        _draw_paths()

    def draw_image(self, gc, x, y, im):
        im = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(im[::-1])
        surface = cairo.ImageSurface.create_for_data(
            im.ravel().data, cairo.FORMAT_ARGB32,
            im.shape[1], im.shape[0], im.shape[1] * 4)
        ctx = gc.ctx
        y = self.height - y - im.shape[0]

        ctx.save()
        ctx.set_source_surface(surface, float(x), float(y))
        ctx.paint()
        ctx.restore()

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # Note: x,y are device/display coords, not user-coords, unlike other
        # draw_* methods
        if ismath:
            self._draw_mathtext(gc, x, y, s, prop, angle)

        else:
            ctx = gc.ctx
            ctx.new_path()
            ctx.move_to(x, y)
            ctx.select_font_face(prop.get_name(),
                                 self.fontangles[prop.get_style()],
                                 self.fontweights[prop.get_weight()])

            size = prop.get_size_in_points() * self.dpi / 72.0

            ctx.save()
            if angle:
                ctx.rotate(np.deg2rad(-angle))
            ctx.set_font_size(size)

            ctx.show_text(s)
            ctx.restore()

    def _draw_mathtext(self, gc, x, y, s, prop, angle):
        ctx = gc.ctx
        width, height, descent, glyphs, rects = self.mathtext_parser.parse(
            s, self.dpi, prop)

        ctx.save()
        ctx.translate(x, y)
        if angle:
            ctx.rotate(np.deg2rad(-angle))

        for font, fontsize, s, ox, oy in glyphs:
            ctx.new_path()
            ctx.move_to(ox, oy)

            fontProp = ttfFontProperty(font)
            ctx.select_font_face(fontProp.name,
                                 self.fontangles[fontProp.style],
                                 self.fontweights[fontProp.weight])

            size = fontsize * self.dpi / 72.0
            ctx.set_font_size(size)
            ctx.show_text(s)

        for ox, oy, w, h in rects:
            ctx.new_path()
            ctx.rectangle(ox, oy, w, h)
            ctx.set_source_rgb(0, 0, 0)
            ctx.fill_preserve()

        ctx.restore()

    def get_canvas_width_height(self):
        return self.width, self.height

    def get_text_width_height_descent(self, s, prop, ismath):
        if ismath:
            width, height, descent, fonts, used_characters = \
                self.mathtext_parser.parse(s, self.dpi, prop)
            return width, height, descent

        ctx = self.text_ctx
        ctx.save()
        ctx.select_font_face(prop.get_name(),
                             self.fontangles[prop.get_style()],
                             self.fontweights[prop.get_weight()])

        # Cairo (says it) uses 1/96 inch user space units, ref: cairo_gstate.c
        # but if /96.0 is used the font is too small
        size = prop.get_size_in_points() * self.dpi / 72

        # problem - scale remembers last setting and font can become
        # enormous causing program to crash
        # save/restore prevents the problem
        ctx.set_font_size(size)

        y_bearing, w, h = ctx.text_extents(s)[1:4]
        ctx.restore()

        return w, h, h + y_bearing

    def new_gc(self):
        self.gc.ctx.save()
        self.gc._alpha = 1
        self.gc._forced_alpha = False # if True, _alpha overrides A from RGBA
        return self.gc

    def points_to_pixels(self, points):
        return points / 72 * self.dpi
