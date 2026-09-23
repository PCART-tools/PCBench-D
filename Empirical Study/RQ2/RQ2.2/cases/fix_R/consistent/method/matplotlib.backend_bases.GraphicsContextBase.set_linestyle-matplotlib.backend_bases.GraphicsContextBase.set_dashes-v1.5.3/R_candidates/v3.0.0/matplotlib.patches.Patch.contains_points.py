    def contains_points(self, points, radius=None):
        """
        Returns a bool array which is ``True`` if the (closed) path
        contains the corresponding point.
        (transformed with its transform attribute).

        *points* must be Nx2 array.
        *radius* allows the path to be made slightly larger or smaller.
        """
        radius = self._process_radius(radius)
        return self.get_path().contains_points(points,
                                               self.get_transform(),
                                               radius)
