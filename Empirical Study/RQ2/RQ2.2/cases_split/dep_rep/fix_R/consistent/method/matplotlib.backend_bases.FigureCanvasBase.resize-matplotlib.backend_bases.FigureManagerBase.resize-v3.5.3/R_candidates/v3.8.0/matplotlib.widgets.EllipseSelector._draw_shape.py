    def _draw_shape(self, extents):
        x0, x1, y0, y1 = extents
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        center = [x0 + (x1 - x0) / 2., y0 + (y1 - y0) / 2.]
        a = (xmax - xmin) / 2.
        b = (ymax - ymin) / 2.

        self._selection_artist.center = center
        self._selection_artist.width = 2 * a
        self._selection_artist.height = 2 * b
        self._selection_artist.angle = self.rotation
