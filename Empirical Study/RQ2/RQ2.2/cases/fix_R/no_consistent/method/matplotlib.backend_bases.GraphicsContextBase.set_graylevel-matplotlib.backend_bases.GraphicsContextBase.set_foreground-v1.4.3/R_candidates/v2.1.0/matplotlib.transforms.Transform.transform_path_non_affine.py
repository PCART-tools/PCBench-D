    def transform_path_non_affine(self, path):
        """
        Returns a path, transformed only by the non-affine
        part of this transform.

        *path*: a :class:`~matplotlib.path.Path` instance.

        ``transform_path(path)`` is equivalent to
        ``transform_path_affine(transform_path_non_affine(values))``.
        """
        x = self.transform_non_affine(path.vertices)
        return Path._fast_from_codes_and_verts(x, path.codes,
                {'interpolation_steps': path._interpolation_steps,
                 'should_simplify': path.should_simplify})
