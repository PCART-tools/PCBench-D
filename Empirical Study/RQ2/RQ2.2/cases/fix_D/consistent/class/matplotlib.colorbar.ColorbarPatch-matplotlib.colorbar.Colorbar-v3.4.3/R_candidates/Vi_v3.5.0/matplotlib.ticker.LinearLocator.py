class LinearLocator(Locator):
    """
    Determine the tick locations

    The first time this function is called it will try to set the
    number of ticks to make a nice tick partitioning.  Thereafter the
    number of ticks will be fixed so that interactive navigation will
    be nice

    """
    def __init__(self, numticks=None, presets=None):
        """
        Use presets to set locs based on lom.  A dict mapping vmin, vmax->locs
        """
        self.numticks = numticks
        if presets is None:
            self.presets = {}
        else:
            self.presets = presets

    @property
    def numticks(self):
        # Old hard-coded default.
        return self._numticks if self._numticks is not None else 11

    @numticks.setter
    def numticks(self, numticks):
        self._numticks = numticks

    def set_params(self, numticks=None, presets=None):
        """Set parameters within this locator."""
        if presets is not None:
            self.presets = presets
        if numticks is not None:
            self.numticks = numticks

    def __call__(self):
        """Return the locations of the ticks."""
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if (vmin, vmax) in self.presets:
            return self.presets[(vmin, vmax)]

        if self.numticks == 0:
            return []
        ticklocs = np.linspace(vmin, vmax, self.numticks)

        return self.raise_if_exceeds(ticklocs)

    def view_limits(self, vmin, vmax):
        """Try to choose the view limits intelligently."""

        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if vmin == vmax:
            vmin -= 1
            vmax += 1

        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            exponent, remainder = divmod(
                math.log10(vmax - vmin), math.log10(max(self.numticks - 1, 1)))
            exponent -= (remainder < .5)
            scale = max(self.numticks - 1, 1) ** (-exponent)
            vmin = math.floor(scale * vmin) / scale
            vmax = math.ceil(scale * vmax) / scale

        return mtransforms.nonsingular(vmin, vmax)
