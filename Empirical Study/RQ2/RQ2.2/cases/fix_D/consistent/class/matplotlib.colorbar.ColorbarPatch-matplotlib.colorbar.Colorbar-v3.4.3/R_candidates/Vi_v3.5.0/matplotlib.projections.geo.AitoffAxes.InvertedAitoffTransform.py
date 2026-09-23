    class InvertedAitoffTransform(_GeoTransform):

        def transform_non_affine(self, xy):
            # docstring inherited
            # MGDTODO: Math is hard ;(
            return np.full_like(xy, np.nan)

        def inverted(self):
            # docstring inherited
            return AitoffAxes.AitoffTransform(self._resolution)
