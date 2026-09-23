@_make_norm_from_scale(
    scale.SymmetricalLogScale,
    init=lambda linthresh, linscale=1., vmin=None, vmax=None, clip=False, *,
                base=10: None)
class SymLogNorm(Normalize):
    """
    The symmetrical logarithmic scale is logarithmic in both the
    positive and negative directions from the origin.

    Since the values close to zero tend toward infinity, there is a
    need to have a range around zero that is linear.  The parameter
    *linthresh* allows the user to specify the size of this range
    (-*linthresh*, *linthresh*).

    Parameters
    ----------
    linthresh : float
        The range within which the plot is linear (to avoid having the plot
        go to infinity around zero).
    linscale : float, default: 1
        This allows the linear range (-*linthresh* to *linthresh*) to be
        stretched relative to the logarithmic range. Its value is the
        number of decades to use for each half of the linear range. For
        example, when *linscale* == 1.0 (the default), the space used for
        the positive and negative halves of the linear range will be equal
        to one decade in the logarithmic range.
    base : float, default: 10
    """

    @property
    def linthresh(self):
        return self._scale.linthresh

    @linthresh.setter
    def linthresh(self, value):
        self._scale.linthresh = value
