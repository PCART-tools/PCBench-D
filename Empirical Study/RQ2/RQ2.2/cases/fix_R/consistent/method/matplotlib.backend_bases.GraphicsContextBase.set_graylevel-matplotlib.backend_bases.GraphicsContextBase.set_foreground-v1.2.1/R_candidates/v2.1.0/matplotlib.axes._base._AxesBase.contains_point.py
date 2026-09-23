    def contains_point(self, point):
        """
        Returns *True* if the point (tuple of x,y) is inside the axes
        (the area defined by the its patch). A pixel coordinate is
        required.

        """
        return self.patch.contains_point(point, radius=1.0)
