    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
        px, py = self.get_offset(w, h, xd, yd, renderer)
        return mtransforms.Bbox.from_bounds(px - xd, py - yd, w, h)
