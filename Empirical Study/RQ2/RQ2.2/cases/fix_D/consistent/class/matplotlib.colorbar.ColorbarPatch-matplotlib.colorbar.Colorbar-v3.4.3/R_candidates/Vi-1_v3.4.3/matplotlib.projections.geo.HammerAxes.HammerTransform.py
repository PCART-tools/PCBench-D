    class HammerTransform(_GeoTransform):
        """The base Hammer transform."""

        def transform_non_affine(self, ll):
            # docstring inherited
            longitude, latitude = ll.T
            half_long = longitude / 2.0
            cos_latitude = np.cos(latitude)
            sqrt2 = np.sqrt(2.0)
            alpha = np.sqrt(1.0 + cos_latitude * np.cos(half_long))
            x = (2.0 * sqrt2) * (cos_latitude * np.sin(half_long)) / alpha
            y = (sqrt2 * np.sin(latitude)) / alpha
            return np.column_stack([x, y])

        def inverted(self):
            # docstring inherited
            return HammerAxes.InvertedHammerTransform(self._resolution)
