    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())

        self.update_scalarmappable()

        transform, offset_trf, offsets, paths = self._prepare_points()

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_snap(self.get_snap())

        if self._hatch:
            gc.set_hatch(self._hatch)
            gc.set_hatch_color(self._hatch_color)

        if self.get_sketch_params() is not None:
            gc.set_sketch_params(*self.get_sketch_params())

        if self.get_path_effects():
            from matplotlib.patheffects import PathEffectRenderer
            renderer = PathEffectRenderer(self.get_path_effects(), renderer)

        # If the collection is made up of a single shape/color/stroke,
        # it can be rendered once and blitted multiple times, using
        # `draw_markers` rather than `draw_path_collection`.  This is
        # *much* faster for Agg, and results in smaller file sizes in
        # PDF/SVG/PS.

        trans = self.get_transforms()
        facecolors = self.get_facecolor()
        edgecolors = self.get_edgecolor()
        do_single_path_optimization = False
        if (len(paths) == 1 and len(trans) <= 1 and
                len(facecolors) == 1 and len(edgecolors) == 1 and
                len(self._linewidths) == 1 and
                all(ls[1] is None for ls in self._linestyles) and
                len(self._antialiaseds) == 1 and len(self._urls) == 1 and
                self.get_hatch() is None):
            if len(trans):
                combined_transform = transforms.Affine2D(trans[0]) + transform
            else:
                combined_transform = transform
            extents = paths[0].get_extents(combined_transform)
            if (extents.width < self.figure.bbox.width
                    and extents.height < self.figure.bbox.height):
                do_single_path_optimization = True

        if self._joinstyle:
            gc.set_joinstyle(self._joinstyle)

        if self._capstyle:
            gc.set_capstyle(self._capstyle)

        if do_single_path_optimization:
            gc.set_foreground(tuple(edgecolors[0]))
            gc.set_linewidth(self._linewidths[0])
            gc.set_dashes(*self._linestyles[0])
            gc.set_antialiased(self._antialiaseds[0])
            gc.set_url(self._urls[0])
            renderer.draw_markers(
                gc, paths[0], combined_transform.frozen(),
                mpath.Path(offsets), offset_trf, tuple(facecolors[0]))
        else:
            renderer.draw_path_collection(
                gc, transform.frozen(), paths,
                self.get_transforms(), offsets, offset_trf,
                self.get_facecolor(), self.get_edgecolor(),
                self._linewidths, self._linestyles,
                self._antialiaseds, self._urls,
                "screen")  # offset_position, kept for backcompat.

        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False
