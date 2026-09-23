    def __call__(self, ax, renderer):
        self.axes = ax

        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        self._update_offset_func(renderer, fontsize)

        width, height, xdescent, ydescent = self.get_extent(renderer)

        px, py = self.get_offset(width, height, 0, 0, renderer)
        bbox_canvas = Bbox.from_bounds(px, py, width, height)
        tr = ax.figure.transFigure.inverted()
        bb = TransformedBbox(bbox_canvas, tr)

        return bb
