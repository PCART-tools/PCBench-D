        def inverted(self):
            return LambertAxes.InvertedLambertTransform(
                self._center_longitude,
                self._center_latitude,
                self._resolution)
