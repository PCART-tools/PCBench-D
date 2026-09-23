class RadialLocator(mticker.Locator):
    """
    Used to locate radius ticks.

    Ensures that all ticks are strictly positive.  For all other tasks, it
    delegates to the base `.Locator` (which may be different depending on the
    scale of the *r*-axis).
    """

    def __init__(self, base, axes=None):
        self.base = base
        self._axes = axes

    def __call__(self):
        show_all = True
        # Ensure previous behaviour with full circle non-annular views.
        if self._axes:
            if _is_full_circle_rad(*self._axes.viewLim.intervalx):
                rorigin = self._axes.get_rorigin() * self._axes.get_rsign()
                if self._axes.get_rmin() <= rorigin:
                    show_all = False
        if show_all:
            return self.base()
        else:
            return [tick for tick in self.base() if tick > rorigin]

    @_api.deprecated("3.3")
    def pan(self, numsteps):
        return self.base.pan(numsteps)

    @_api.deprecated("3.3")
    def zoom(self, direction):
        return self.base.zoom(direction)

    @_api.deprecated("3.3")
    def refresh(self):
        # docstring inherited
        return self.base.refresh()

    def nonsingular(self, vmin, vmax):
        # docstring inherited
        return ((0, 1) if (vmin, vmax) == (-np.inf, np.inf)  # Init. limits.
                else self.base.nonsingular(vmin, vmax))

    def view_limits(self, vmin, vmax):
        vmin, vmax = self.base.view_limits(vmin, vmax)
        if vmax > vmin:
            # this allows inverted r/y-lims
            vmin = min(0, vmin)
        return mtransforms.nonsingular(vmin, vmax)
