    def get_window_extent(self, renderer):
        # docstring inherited
        w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
        px, py = self.get_offset(w, h, xd, yd, renderer)
        return mtransforms.Bbox.from_bounds(px - xd, py - yd, w, h)
