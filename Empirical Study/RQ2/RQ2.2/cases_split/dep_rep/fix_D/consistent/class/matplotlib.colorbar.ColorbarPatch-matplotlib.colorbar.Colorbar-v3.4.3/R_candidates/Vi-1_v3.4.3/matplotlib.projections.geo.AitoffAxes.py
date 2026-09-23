class AitoffAxes(GeoAxes):
    name = 'aitoff'

    class AitoffTransform(_GeoTransform):
        """The base Aitoff transform."""

        def transform_non_affine(self, ll):
            # docstring inherited
            longitude, latitude = ll.T

            # Pre-compute some values
            half_long = longitude / 2.0
            cos_latitude = np.cos(latitude)

            alpha = np.arccos(cos_latitude * np.cos(half_long))
            sinc_alpha = np.sinc(alpha / np.pi)  # np.sinc is sin(pi*x)/(pi*x).

            x = (cos_latitude * np.sin(half_long)) / sinc_alpha
            y = np.sin(latitude) / sinc_alpha
            return np.column_stack([x, y])

        def inverted(self):
            # docstring inherited
            return AitoffAxes.InvertedAitoffTransform(self._resolution)

    class InvertedAitoffTransform(_GeoTransform):

        def transform_non_affine(self, xy):
            # docstring inherited
            # MGDTODO: Math is hard ;(
            return np.full_like(xy, np.nan)

        def inverted(self):
            # docstring inherited
            return AitoffAxes.AitoffTransform(self._resolution)

    def __init__(self, *args, **kwargs):
        self._longitude_cap = np.pi / 2.0
        super().__init__(*args, **kwargs)
        self.set_aspect(0.5, adjustable='box', anchor='C')
        self.cla()

    def _get_core_transform(self, resolution):
        return self.AitoffTransform(resolution)
