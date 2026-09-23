    def transform_path_non_affine(self, path):
        if self._a.is_affine and self._b.is_affine:
            return path
        elif not self._a.is_affine and self._b.is_affine:
            return self._a.transform_path_non_affine(path)
        else:
            return self._b.transform_path_non_affine(
                                    self._a.transform_path(path))
