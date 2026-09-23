    @property
    def width(self):
        """The (signed) width of the bounding box."""
        points = self.get_points()
        return points[1, 0] - points[0, 0]
