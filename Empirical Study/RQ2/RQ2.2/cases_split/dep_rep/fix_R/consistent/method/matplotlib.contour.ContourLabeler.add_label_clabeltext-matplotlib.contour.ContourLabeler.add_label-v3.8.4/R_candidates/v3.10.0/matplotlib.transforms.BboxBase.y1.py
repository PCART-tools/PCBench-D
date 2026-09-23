    @property
    def y1(self):
        """
        The second of the pair of *y* coordinates that define the bounding box.

        This is not guaranteed to be greater than :attr:`y0` (for that, use
        :attr:`ymax`).
        """
        return self.get_points()[1, 1]
