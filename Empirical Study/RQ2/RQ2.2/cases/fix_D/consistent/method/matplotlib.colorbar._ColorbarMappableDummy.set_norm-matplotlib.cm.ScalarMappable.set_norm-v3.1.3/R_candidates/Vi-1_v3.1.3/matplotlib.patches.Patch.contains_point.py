    def contains_point(self, point, radius=None):
        """
        Returns ``True`` if the given *point* is inside the path
        (transformed with its transform attribute).

        *radius* allows the path to be made slightly larger or smaller.
        """
        radius = self._process_radius(radius)
        return self.get_path().contains_point(point,
                                              self.get_transform(),
                                              radius)
