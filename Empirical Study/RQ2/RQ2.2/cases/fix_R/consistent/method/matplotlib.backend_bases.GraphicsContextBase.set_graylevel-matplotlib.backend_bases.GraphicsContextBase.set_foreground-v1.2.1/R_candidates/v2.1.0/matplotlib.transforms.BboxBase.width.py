    @property
    def width(self):
        """
        (property) The width of the bounding box.  It may be negative if
        :attr:`x1` < :attr:`x0`.
        """
        points = self.get_points()
        return points[1, 0] - points[0, 0]
