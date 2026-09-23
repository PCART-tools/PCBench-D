    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset()
        return mtransforms.Bbox.from_bounds(ox - xd, oy - yd, w, h)
