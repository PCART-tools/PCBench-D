class PolarAffine(mtransforms.Affine2DBase):
    """
    The affine part of the polar projection.  Scales the output so
    that maximum radius rests on the edge of the axes circle.
    """
    def __init__(self, scale_transform, limits):
        """
        *limits* is the view limit of the data.  The only part of
        its bounds that is used is the y limits (for the radius limits).
        The theta range is handled by the non-affine transform.
        """
        super().__init__()
        self._scale_transform = scale_transform
        self._limits = limits
        self.set_children(scale_transform, limits)
        self._mtx = None

    __str__ = mtransforms._make_str_method("_scale_transform", "_limits")

    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            limits_scaled = self._limits.transformed(self._scale_transform)
            yscale = limits_scaled.ymax - limits_scaled.ymin
            affine = mtransforms.Affine2D() \
                .scale(0.5 / yscale) \
                .translate(0.5, 0.5)
            self._mtx = affine.get_matrix()
            self._inverted = None
            self._invalid = 0
        return self._mtx
