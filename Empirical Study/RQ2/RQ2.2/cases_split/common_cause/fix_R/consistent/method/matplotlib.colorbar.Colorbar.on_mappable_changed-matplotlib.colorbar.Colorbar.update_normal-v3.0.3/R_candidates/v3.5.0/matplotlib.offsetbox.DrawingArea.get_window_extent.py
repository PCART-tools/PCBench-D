    def get_window_extent(self, renderer):
        # docstring inherited
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset()  # w, h, xd, yd)

        return mtransforms.Bbox.from_bounds(ox - xd, oy - yd, w, h)
