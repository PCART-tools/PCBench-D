class _ColorbarAutoMinorLocator(ticker.AutoMinorLocator):
    """
    AutoMinorLocator for Colorbar

    This locator is just a `.AutoMinorLocator` except the min and max are
    clipped by the norm's min and max (i.e. vmin/vmax from the
    image/pcolor/contour object).  This is necessary so that the minorticks
    don't extrude into the "extend regions".
    """

    def __init__(self, colorbar, n=None):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.
        """
        self._colorbar = colorbar
        self.ndivs = n
        super().__init__(n=None)

    def __call__(self):
        vmin = self._colorbar.norm.vmin
        vmax = self._colorbar.norm.vmax
        ticks = super().__call__()
        rtol = (vmax - vmin) * 1e-10
        return ticks[(ticks >= vmin - rtol) & (ticks <= vmax + rtol)]
