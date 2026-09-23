    @property
    def extents(self):
        """Return (:attr:`x0`, :attr:`y0`, :attr:`x1`, :attr:`y1`)."""
        return self.get_points().flatten()  # flatten returns a copy.
