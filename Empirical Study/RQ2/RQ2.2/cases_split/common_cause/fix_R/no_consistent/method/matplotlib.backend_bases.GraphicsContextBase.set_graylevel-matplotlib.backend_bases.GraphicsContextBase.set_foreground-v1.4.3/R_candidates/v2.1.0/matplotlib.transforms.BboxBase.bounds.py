    @property
    def bounds(self):
        """
        (property) Returns (:attr:`x0`, :attr:`y0`, :attr:`width`,
        :attr:`height`).
        """
        x0, y0, x1, y1 = self.get_points().flatten()
        return (x0, y0, x1 - x0, y1 - y0)
