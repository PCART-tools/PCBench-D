    def get_window_extent(self, renderer):
        # docstring inherited
        self._update_offset_func(renderer)
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset(w, h, xd, yd, renderer)
        return Bbox.from_bounds(ox - xd, oy - yd, w, h)
