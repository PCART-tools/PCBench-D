class InvertedPolarTransform(mtransforms.Transform):
    """
    The inverse of the polar transform, mapping Cartesian
    coordinate space *x* and *y* back to *theta* and *r*.
    """
    input_dims = output_dims = 2

    def __init__(self, axis=None, use_rmin=True,
                 _apply_theta_transforms=True):
        super().__init__()
        self._axis = axis
        self._use_rmin = use_rmin
        self._apply_theta_transforms = _apply_theta_transforms

    __str__ = mtransforms._make_str_method(
        "_axis",
        use_rmin="_use_rmin",
        _apply_theta_transforms="_apply_theta_transforms")

    def transform_non_affine(self, xy):
        # docstring inherited
        x, y = xy.T
        r = np.hypot(x, y)
        theta = (np.arctan2(y, x) + 2 * np.pi) % (2 * np.pi)
        # PolarAxes does not use the theta transforms here, but apply them for
        # backwards-compatibility if not being used by it.
        if self._apply_theta_transforms and self._axis is not None:
            theta -= self._axis.get_theta_offset()
            theta *= self._axis.get_theta_direction()
            theta %= 2 * np.pi
        if self._use_rmin and self._axis is not None:
            r += self._axis.get_rorigin()
            r *= self._axis.get_rsign()
        return np.column_stack([theta, r])

    def inverted(self):
        # docstring inherited
        return PolarAxes.PolarTransform(self._axis, self._use_rmin,
                                        self._apply_theta_transforms)
