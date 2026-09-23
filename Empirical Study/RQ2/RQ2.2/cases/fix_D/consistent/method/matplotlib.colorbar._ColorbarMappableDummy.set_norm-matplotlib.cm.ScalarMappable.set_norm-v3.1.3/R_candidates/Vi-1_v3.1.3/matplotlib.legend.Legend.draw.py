    @allow_rasterization
    def draw(self, renderer):
        "Draw everything that belongs to the legend."
        if not self.get_visible():
            return

        renderer.open_group('legend')

        fontsize = renderer.points_to_pixels(self._fontsize)

        # if mode == fill, set the width of the legend_box to the
        # width of the parent (minus pads)
        if self._mode in ["expand"]:
            pad = 2 * (self.borderaxespad + self.borderpad) * fontsize
            self._legend_box.set_width(self.get_bbox_to_anchor().width - pad)

        # update the location and size of the legend. This needs to
        # be done in any case to clip the figure right.
        bbox = self._legend_box.get_window_extent(renderer)
        self.legendPatch.set_bounds(bbox.x0, bbox.y0,
                                    bbox.width, bbox.height)
        self.legendPatch.set_mutation_scale(fontsize)

        if self._drawFrame:
            if self.shadow:
                shadow = Shadow(self.legendPatch, 2, -2)
                shadow.draw(renderer)

            self.legendPatch.draw(renderer)

        self._legend_box.draw(renderer)

        renderer.close_group('legend')
        self.stale = False
