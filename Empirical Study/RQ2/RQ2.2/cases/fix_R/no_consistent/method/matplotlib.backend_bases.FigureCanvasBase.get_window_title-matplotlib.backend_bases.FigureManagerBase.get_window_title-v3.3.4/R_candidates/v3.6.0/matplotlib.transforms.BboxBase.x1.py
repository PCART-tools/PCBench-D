    @property
    def x1(self):
        """
        The second of the pair of *x* coordinates that define the bounding box.

        This is not guaranteed to be greater than :attr:`x0` (for that, use
        :attr:`xmax`).
        """
        return self.get_points()[1, 0]
