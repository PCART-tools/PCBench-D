    def _revalidate(self):
        patch_path = self._patch.get_path()
        # Only recompute if the invalidation includes the non_affine part of
        # the transform, or the Patch's Path has changed.
        if (self._transformed_path is None or self._path != patch_path or
                (self._invalid & self.INVALID_NON_AFFINE ==
                    self.INVALID_NON_AFFINE)):
            self._path = patch_path
            self._transformed_path = \
                self._transform.transform_path_non_affine(patch_path)
            self._transformed_points = \
                Path._fast_from_codes_and_verts(
                    self._transform.transform_non_affine(patch_path.vertices),
                    None, patch_path)
        self._invalid = 0
