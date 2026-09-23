class MultipleLocator(Locator):
    """
    Set a tick on each integer multiple of a base within the view interval.
    """

    def __init__(self, base=1.0):
        self._edge = _Edge_integer(base, 0)

    def set_params(self, base):
        """Set parameters within this locator."""
        if base is not None:
            self._edge = _Edge_integer(base, 0)

    def __call__(self):
        """Return the locations of the ticks."""
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        if vmax < vmin:
            vmin, vmax = vmax, vmin
        step = self._edge.step
        vmin = self._edge.ge(vmin) * step
        n = (vmax - vmin + 0.001 * step) // step
        locs = vmin - step + np.arange(n + 3) * step
        return self.raise_if_exceeds(locs)

    def view_limits(self, dmin, dmax):
        """
        Set the view limits to the nearest multiples of base that
        contain the data.
        """
        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = self._edge.le(dmin) * self._edge.step
            vmax = self._edge.ge(dmax) * self._edge.step
            if vmin == vmax:
                vmin -= 1
                vmax += 1
        else:
            vmin = dmin
            vmax = dmax

        return mtransforms.nonsingular(vmin, vmax)
