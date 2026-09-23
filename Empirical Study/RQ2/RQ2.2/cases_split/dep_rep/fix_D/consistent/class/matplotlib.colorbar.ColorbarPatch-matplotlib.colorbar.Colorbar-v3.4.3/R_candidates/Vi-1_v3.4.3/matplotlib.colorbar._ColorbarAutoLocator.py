class _ColorbarAutoLocator(ticker.MaxNLocator):
    """
    AutoLocator for Colorbar

    This locator is just a `.MaxNLocator` except the min and max are
    clipped by the norm's min and max (i.e. vmin/vmax from the
    image/pcolor/contour object).  This is necessary so ticks don't
    extrude into the "extend regions".
    """

    def __init__(self, colorbar):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.  Otherwise it is the same as
        `~.ticker.AutoLocator`.
        """

        self._colorbar = colorbar
        nbins = 'auto'
        steps = [1, 2, 2.5, 5, 10]
        super().__init__(nbins=nbins, steps=steps)

    def tick_values(self, vmin, vmax):
        # flip if needed:
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        vmin = max(vmin, self._colorbar.norm.vmin)
        vmax = min(vmax, self._colorbar.norm.vmax)
        ticks = super().tick_values(vmin, vmax)
        rtol = (vmax - vmin) * 1e-10
        return ticks[(ticks >= vmin - rtol) & (ticks <= vmax + rtol)]
