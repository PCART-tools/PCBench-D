class SymmetricalLogScale(ScaleBase):
    """
    The symmetrical logarithmic scale is logarithmic in both the
    positive and negative directions from the origin.

    Since the values close to zero tend toward infinity, there is a
    need to have a range around zero that is linear.  The parameter
    *linthresh* allows the user to specify the size of this range
    (-*linthresh*, *linthresh*).

    Parameters
    ----------
    base : float, default: 10
        The base of the logarithm.

    linthresh : float, default: 2
        Defines the range ``(-x, x)``, within which the plot is linear.
        This avoids having the plot go to infinity around zero.

    subs : sequence of int
        Where to place the subticks between each major tick.
        For example, in a log10 scale: ``[2, 3, 4, 5, 6, 7, 8, 9]`` will place
        8 logarithmically spaced minor ticks between each major tick.

    linscale : float, optional
        This allows the linear range ``(-linthresh, linthresh)`` to be
        stretched relative to the logarithmic range. Its value is the number of
        decades to use for each half of the linear range. For example, when
        *linscale* == 1.0 (the default), the space used for the positive and
        negative halves of the linear range will be equal to one decade in
        the logarithmic range.
    """
    name = 'symlog'

    @_api.deprecated("3.3", alternative="scale.SymmetricalLogTransform")
    @property
    def SymmetricalLogTransform(self):
        return SymmetricalLogTransform

    @_api.deprecated(
        "3.3", alternative="scale.InvertedSymmetricalLogTransform")
    @property
    def InvertedSymmetricalLogTransform(self):
        return InvertedSymmetricalLogTransform

    def __init__(self, axis, **kwargs):
        axis_name = getattr(axis, "axis_name", "x")
        # See explanation in LogScale.__init__.
        @_api.rename_parameter("3.3", f"base{axis_name}", "base")
        @_api.rename_parameter("3.3", f"linthresh{axis_name}", "linthresh")
        @_api.rename_parameter("3.3", f"subs{axis_name}", "subs")
        @_api.rename_parameter("3.3", f"linscale{axis_name}", "linscale")
        def __init__(*, base=10, linthresh=2, subs=None, linscale=1):
            return base, linthresh, subs, linscale

        base, linthresh, subs, linscale = __init__(**kwargs)
        self._transform = SymmetricalLogTransform(base, linthresh, linscale)
        self.subs = subs

    base = property(lambda self: self._transform.base)
    linthresh = property(lambda self: self._transform.linthresh)
    linscale = property(lambda self: self._transform.linscale)

    def set_default_locators_and_formatters(self, axis):
        # docstring inherited
        axis.set_major_locator(SymmetricalLogLocator(self.get_transform()))
        axis.set_major_formatter(LogFormatterSciNotation(self.base))
        axis.set_minor_locator(SymmetricalLogLocator(self.get_transform(),
                                                     self.subs))
        axis.set_minor_formatter(NullFormatter())

    def get_transform(self):
        """Return the `.SymmetricalLogTransform` associated with this scale."""
        return self._transform
