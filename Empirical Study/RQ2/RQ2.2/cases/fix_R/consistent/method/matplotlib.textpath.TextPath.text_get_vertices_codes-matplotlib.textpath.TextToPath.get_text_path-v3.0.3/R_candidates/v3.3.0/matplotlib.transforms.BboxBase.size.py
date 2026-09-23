    @property
    def size(self):
        """The (signed) width and height of the bounding box."""
        points = self.get_points()
        return points[1] - points[0]
