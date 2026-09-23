    def contains_point(self, point):
        """
        Return whether *point* (pair of pixel coordinates) is inside the Axes
        patch.
        """
        return self.patch.contains_point(point, radius=1.0)
