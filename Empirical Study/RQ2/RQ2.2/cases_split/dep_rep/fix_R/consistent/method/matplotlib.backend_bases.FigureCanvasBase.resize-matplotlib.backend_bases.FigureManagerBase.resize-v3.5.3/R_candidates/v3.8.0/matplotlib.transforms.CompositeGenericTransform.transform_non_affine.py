    @_api.rename_parameter("3.8", "points", "values")
    def transform_non_affine(self, values):
        # docstring inherited
        if self._a.is_affine and self._b.is_affine:
            return values
        elif not self._a.is_affine and self._b.is_affine:
            return self._a.transform_non_affine(values)
        else:
            return self._b.transform_non_affine(self._a.transform(values))
