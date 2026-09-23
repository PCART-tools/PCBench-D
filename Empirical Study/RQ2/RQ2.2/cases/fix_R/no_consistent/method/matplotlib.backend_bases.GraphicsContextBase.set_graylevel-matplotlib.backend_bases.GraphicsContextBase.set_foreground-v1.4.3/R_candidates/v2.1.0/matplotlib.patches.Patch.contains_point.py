    def contains_point(self, point, radius=None):
        """
        Returns *True* if the given point is inside the path
        (transformed with its transform attribute).
        """
        radius = self._process_radius(radius)
        return self.get_path().contains_point(point,
                                              self.get_transform(),
                                              radius)
