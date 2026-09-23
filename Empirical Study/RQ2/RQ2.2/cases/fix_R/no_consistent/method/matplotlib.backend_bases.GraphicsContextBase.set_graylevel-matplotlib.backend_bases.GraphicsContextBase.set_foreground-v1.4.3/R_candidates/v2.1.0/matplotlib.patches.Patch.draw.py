    @allow_rasterization
    def draw(self, renderer):
        'Draw the :class:`Patch` to the given *renderer*.'
        if not self.get_visible():
            return

        renderer.open_group('patch', self.get_gid())
        gc = renderer.new_gc()

        gc.set_foreground(self._edgecolor, isRGBA=True)

        lw = self._linewidth
        if self._edgecolor[3] == 0:
            lw = 0
        gc.set_linewidth(lw)
        gc.set_dashes(0, self._dashes)
        gc.set_capstyle(self._capstyle)
        gc.set_joinstyle(self._joinstyle)

        gc.set_antialiased(self._antialiased)
        self._set_gc_clip(gc)
        gc.set_url(self._url)
        gc.set_snap(self.get_snap())

        rgbFace = self._facecolor
        if rgbFace[3] == 0:
            rgbFace = None  # (some?) renderers expect this as no-fill signal

        gc.set_alpha(self._alpha)

        if self._hatch:
            gc.set_hatch(self._hatch)
            try:
                gc.set_hatch_color(self._hatch_color)
            except AttributeError:
                # if we end up with a GC that does not have this method
                warnings.warn("Your backend does not have support for "
                              "setting the hatch color.")

        if self.get_sketch_params() is not None:
            gc.set_sketch_params(*self.get_sketch_params())

        path = self.get_path()
        transform = self.get_transform()
        tpath = transform.transform_path_non_affine(path)
        affine = transform.get_affine()

        if self.get_path_effects():
            from matplotlib.patheffects import PathEffectRenderer
            renderer = PathEffectRenderer(self.get_path_effects(), renderer)

        renderer.draw_path(gc, tpath, affine, rgbFace)

        gc.restore()
        renderer.close_group('patch')
        self.stale = False
