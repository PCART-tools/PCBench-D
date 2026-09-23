    def transform_non_affine(self, points):
        # docstring inherited
        if self._a.is_affine and self._b.is_affine:
            return points
        elif not self._a.is_affine and self._b.is_affine:
            return self._a.transform_non_affine(points)
        else:
            return self._b.transform_non_affine(
                                self._a.transform(points))
