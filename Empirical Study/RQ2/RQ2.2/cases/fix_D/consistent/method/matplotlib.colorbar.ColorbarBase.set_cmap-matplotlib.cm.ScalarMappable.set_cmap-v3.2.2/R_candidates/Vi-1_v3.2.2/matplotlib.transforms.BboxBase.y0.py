    @property
    def y0(self):
        """
        The first of the pair of *y* coordinates that define the bounding box.

        This is not guaranteed to be less than :attr:`y1` (for that, use
        :attr:`ymin`).
        """
        return self.get_points()[0, 1]
