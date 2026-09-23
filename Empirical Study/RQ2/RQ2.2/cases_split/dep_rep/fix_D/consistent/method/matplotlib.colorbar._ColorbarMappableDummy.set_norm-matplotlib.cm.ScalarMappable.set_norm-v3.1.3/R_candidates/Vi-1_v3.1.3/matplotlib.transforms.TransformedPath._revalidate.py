    def _revalidate(self):
        # only recompute if the invalidation includes the non_affine part of the transform
        if ((self._invalid & self.INVALID_NON_AFFINE == self.INVALID_NON_AFFINE)
            or self._transformed_path is None):
            self._transformed_path = \
                self._transform.transform_path_non_affine(self._path)
            self._transformed_points = \
                Path._fast_from_codes_and_verts(
                    self._transform.transform_non_affine(self._path.vertices),
                    None, self._path)
        self._invalid = 0
