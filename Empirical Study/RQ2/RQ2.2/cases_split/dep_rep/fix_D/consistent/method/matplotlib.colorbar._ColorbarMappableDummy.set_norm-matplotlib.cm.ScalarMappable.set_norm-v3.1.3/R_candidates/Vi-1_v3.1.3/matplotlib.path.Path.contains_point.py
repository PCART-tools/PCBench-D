    def contains_point(self, point, transform=None, radius=0.0):
        """
        Returns whether the (closed) path contains the given point.

        If *transform* is not ``None``, the path will be transformed before
        performing the test.

        *radius* allows the path to be made slightly larger or smaller.
        """
        if transform is not None:
            transform = transform.frozen()
        # `point_in_path` does not handle nonlinear transforms, so we
        # transform the path ourselves.  If `transform` is affine, letting
        # `point_in_path` handle the transform avoids allocating an extra
        # buffer.
        if transform and not transform.is_affine:
            self = transform.transform_path(self)
            transform = None
        return _path.point_in_path(point[0], point[1], radius, self, transform)
