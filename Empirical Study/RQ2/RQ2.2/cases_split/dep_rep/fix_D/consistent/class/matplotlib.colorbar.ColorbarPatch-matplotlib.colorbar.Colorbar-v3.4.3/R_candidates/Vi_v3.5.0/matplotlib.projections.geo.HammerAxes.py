class HammerAxes(GeoAxes):
    name = 'hammer'

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

    class InvertedHammerTransform(_GeoTransform):

        def transform_non_affine(self, xy):
            # docstring inherited
            x, y = xy.T
            z = np.sqrt(1 - (x / 4) ** 2 - (y / 2) ** 2)
            longitude = 2 * np.arctan((z * x) / (2 * (2 * z ** 2 - 1)))
            latitude = np.arcsin(y*z)
            return np.column_stack([longitude, latitude])

        def inverted(self):
            # docstring inherited
            return HammerAxes.HammerTransform(self._resolution)

    def __init__(self, *args, **kwargs):
        self._longitude_cap = np.pi / 2.0
        super().__init__(*args, **kwargs)
        self.set_aspect(0.5, adjustable='box', anchor='C')
        self.cla()

    def _get_core_transform(self, resolution):
        return self.HammerTransform(resolution)
