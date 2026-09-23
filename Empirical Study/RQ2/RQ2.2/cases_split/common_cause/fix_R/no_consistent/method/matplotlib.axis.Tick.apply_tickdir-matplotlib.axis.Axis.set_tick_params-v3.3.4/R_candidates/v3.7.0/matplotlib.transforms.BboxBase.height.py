    @property
    def height(self):
        """The (signed) height of the bounding box."""
        points = self.get_points()
        return points[1, 1] - points[0, 1]
