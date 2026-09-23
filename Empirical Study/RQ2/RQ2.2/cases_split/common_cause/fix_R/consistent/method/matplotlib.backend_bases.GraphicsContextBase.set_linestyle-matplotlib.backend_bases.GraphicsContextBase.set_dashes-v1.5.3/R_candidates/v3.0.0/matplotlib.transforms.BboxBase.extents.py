    @property
    def extents(self):
        """
        Returns (:attr:`x0`, :attr:`y0`, :attr:`x1`,
        :attr:`y1`).
        """
        return self.get_points().flatten().copy()
