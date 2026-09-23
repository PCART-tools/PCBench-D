        def inverted(self):
            # docstring inherited
            return LambertAxes.LambertTransform(
                self._center_longitude,
                self._center_latitude,
                self._resolution)
