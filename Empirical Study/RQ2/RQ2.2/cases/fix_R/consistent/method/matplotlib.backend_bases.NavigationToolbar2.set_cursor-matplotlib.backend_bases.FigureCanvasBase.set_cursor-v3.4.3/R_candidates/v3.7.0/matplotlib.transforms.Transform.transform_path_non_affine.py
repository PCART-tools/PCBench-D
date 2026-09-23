    def transform_path_non_affine(self, path):
        """
        Apply the non-affine part of this transform to `.Path` *path*,
        returning a new `.Path`.

        ``transform_path(path)`` is equivalent to
        ``transform_path_affine(transform_path_non_affine(values))``.
        """
        x = self.transform_non_affine(path.vertices)
        return Path._fast_from_codes_and_verts(x, path.codes, path)
