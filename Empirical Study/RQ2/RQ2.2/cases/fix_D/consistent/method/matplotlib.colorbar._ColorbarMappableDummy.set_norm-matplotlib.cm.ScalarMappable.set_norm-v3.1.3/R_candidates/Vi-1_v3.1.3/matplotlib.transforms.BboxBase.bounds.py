    @property
    def bounds(self):
        """Return (:attr:`x0`, :attr:`y0`, :attr:`width`, :attr:`height`)."""
        (x0, y0), (x1, y1) = self.get_points()
        return (x0, y0, x1 - x0, y1 - y0)
