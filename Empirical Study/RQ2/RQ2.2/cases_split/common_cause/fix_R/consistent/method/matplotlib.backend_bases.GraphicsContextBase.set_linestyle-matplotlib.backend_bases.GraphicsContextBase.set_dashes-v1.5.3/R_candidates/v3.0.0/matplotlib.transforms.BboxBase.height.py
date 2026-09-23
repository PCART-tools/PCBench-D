    @property
    def height(self):
        """
        The height of the bounding box.  It may be negative if
        :attr:`y1` < :attr:`y0`.
        """
        points = self.get_points()
        return points[1, 1] - points[0, 1]
