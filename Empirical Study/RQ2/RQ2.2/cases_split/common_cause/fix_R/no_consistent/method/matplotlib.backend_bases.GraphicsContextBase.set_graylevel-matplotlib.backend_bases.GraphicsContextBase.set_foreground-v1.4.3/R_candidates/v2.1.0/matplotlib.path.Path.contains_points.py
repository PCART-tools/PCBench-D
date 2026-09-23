    def contains_points(self, points, transform=None, radius=0.0):
        """
        Returns a bool array which is ``True`` if the (closed) path contains
        the corresponding point.

        If *transform* is not ``None``, the path will be transformed before
        performing the test.

        *radius* allows the path to be made slightly larger or smaller.
        """
        if transform is not None:
            transform = transform.frozen()
        result = _path.points_in_path(points, radius, self, transform)
        return result.astype('bool')
