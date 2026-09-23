    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())

        self.update_scalarmappable()

        transform, transOffset, offsets, paths = self._prepare_points()

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_snap(self.get_snap())

        if self._hatch:
            gc.set_hatch(self._hatch)
            try:
                gc.set_hatch_color(self._hatch_color)
            except AttributeError:
                # if we end up with a GC that does not have this method
                warnings.warn("Your backend does not support setting the "
                              "hatch color.")

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
            self._linestyles == [(None, None)] and
            len(self._antialiaseds) == 1 and len(self._urls) == 1 and
            self.get_hatch() is None):
            if len(trans):
                combined_transform = (transforms.Affine2D(trans[0]) +
                                      transform)
            else:
                combined_transform = transform
            extents = paths[0].get_extents(combined_transform)
            width, height = renderer.get_canvas_width_height()
            if (extents.width < width and
                extents.height < height):
                do_single_path_optimization = True

        if do_single_path_optimization:
            gc.set_foreground(tuple(edgecolors[0]))
            gc.set_linewidth(self._linewidths[0])
            gc.set_dashes(*self._linestyles[0])
            gc.set_antialiased(self._antialiaseds[0])
            gc.set_url(self._urls[0])
            renderer.draw_markers(
                gc, paths[0], combined_transform.frozen(),
                mpath.Path(offsets), transOffset, tuple(facecolors[0]))
        else:
            renderer.draw_path_collection(
                gc, transform.frozen(), paths,
                self.get_transforms(), offsets, transOffset,
                self.get_facecolor(), self.get_edgecolor(),
                self._linewidths, self._linestyles,
                self._antialiaseds, self._urls,
                self._offset_position)

        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False
