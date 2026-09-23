    @property
    def extents(self):
        """
        (property) Returns (:attr:`x0`, :attr:`y0`, :attr:`x1`,
        :attr:`y1`).
        """
        return self.get_points().flatten().copy()
