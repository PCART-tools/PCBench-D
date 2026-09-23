    def transform_path_affine(self, path):
        """
        Returns a path, transformed only by the affine part of
        this transform.

        *path*: a :class:`~matplotlib.path.Path` instance.

        ``transform_path(path)`` is equivalent to
        ``transform_path_affine(transform_path_non_affine(values))``.
        """
        return self.get_affine().transform_path_affine(path)
