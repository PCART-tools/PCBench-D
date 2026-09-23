@make_norm_from_scale(
    scale.AsinhScale,
    init=lambda linear_width=1, vmin=None, vmax=None, clip=False: None)
class AsinhNorm(Normalize):
    """
    The inverse hyperbolic sine scale is approximately linear near
    the origin, but becomes logarithmic for larger positive
    or negative values. Unlike the `SymLogNorm`, the transition between
    these linear and logarithmic regions is smooth, which may reduce
    the risk of visual artifacts.

    .. note::

       This API is provisional and may be revised in the future
       based on early user feedback.

    Parameters
    ----------
    linear_width : float, default: 1
        The effective width of the linear region, beyond which
        the transformation becomes asymptotically logarithmic
    """

    @property
    def linear_width(self):
        return self._scale.linear_width

    @linear_width.setter
    def linear_width(self, value):
        self._scale.linear_width = value
