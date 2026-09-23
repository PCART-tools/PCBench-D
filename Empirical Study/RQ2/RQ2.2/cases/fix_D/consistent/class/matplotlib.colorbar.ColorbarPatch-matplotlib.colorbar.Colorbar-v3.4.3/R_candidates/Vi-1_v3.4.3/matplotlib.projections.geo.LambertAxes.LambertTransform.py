    class LambertTransform(_GeoTransform):
        """The base Lambert transform."""

        def __init__(self, center_longitude, center_latitude, resolution):
            """
            Create a new Lambert transform.  Resolution is the number of steps
            to interpolate between each input line segment to approximate its
            path in curved Lambert space.
            """
            _GeoTransform.__init__(self, resolution)
            self._center_longitude = center_longitude
            self._center_latitude = center_latitude

        def transform_non_affine(self, ll):
            # docstring inherited
            longitude, latitude = ll.T
            clong = self._center_longitude
            clat = self._center_latitude
            cos_lat = np.cos(latitude)
            sin_lat = np.sin(latitude)
            diff_long = longitude - clong
            cos_diff_long = np.cos(diff_long)

            inner_k = np.maximum(  # Prevent divide-by-zero problems
                1 + np.sin(clat)*sin_lat + np.cos(clat)*cos_lat*cos_diff_long,
                1e-15)
            k = np.sqrt(2 / inner_k)
            x = k * cos_lat*np.sin(diff_long)
            y = k * (np.cos(clat)*sin_lat - np.sin(clat)*cos_lat*cos_diff_long)

            return np.column_stack([x, y])

        def inverted(self):
            # docstring inherited
            return LambertAxes.InvertedLambertTransform(
                self._center_longitude,
                self._center_latitude,
                self._resolution)
