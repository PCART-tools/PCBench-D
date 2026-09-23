    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        ctx = gc.ctx
        # Clip the path to the actual rendering extents if it isn't filled.
        clip = (ctx.clip_extents()
                if rgbFace is None and gc.get_hatch() is None
                else None)
        transform = (transform
                     + Affine2D().scale(1, -1).translate(0, self.height))
        ctx.new_path()
        _append_path(ctx, path, transform, clip)
        if rgbFace is not None:
            ctx.save()
            _set_rgba(ctx, rgbFace, gc.get_alpha(), gc.get_forced_alpha())
            ctx.fill_preserve()
            ctx.restore()
        hatch_path = gc.get_hatch_path()
        if hatch_path:
            dpi = int(self.dpi)
            hatch_surface = ctx.get_target().create_similar(
                cairo.Content.COLOR_ALPHA, dpi, dpi)
            hatch_ctx = cairo.Context(hatch_surface)
            _append_path(hatch_ctx, hatch_path,
                         Affine2D().scale(dpi, -dpi).translate(0, dpi),
                         None)
            hatch_ctx.set_line_width(self.points_to_pixels(gc.get_hatch_linewidth()))
            hatch_ctx.set_source_rgba(*gc.get_hatch_color())
            hatch_ctx.fill_preserve()
            hatch_ctx.stroke()
            hatch_pattern = cairo.SurfacePattern(hatch_surface)
            hatch_pattern.set_extend(cairo.Extend.REPEAT)
            ctx.save()
            ctx.set_source(hatch_pattern)
            ctx.fill_preserve()
            ctx.restore()
        ctx.stroke()
