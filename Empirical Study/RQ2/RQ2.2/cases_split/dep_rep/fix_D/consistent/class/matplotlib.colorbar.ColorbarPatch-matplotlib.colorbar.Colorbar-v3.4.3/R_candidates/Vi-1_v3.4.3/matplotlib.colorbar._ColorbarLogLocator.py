class _ColorbarLogLocator(ticker.LogLocator):
    """
    LogLocator for Colorbarbar

    This locator is just a `.LogLocator` except the min and max are
    clipped by the norm's min and max (i.e. vmin/vmax from the
    image/pcolor/contour object).  This is necessary so ticks don't
    extrude into the "extend regions".

    """
    def __init__(self, colorbar, *args, **kwargs):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.  Otherwise it is the same as
        `~.ticker.LogLocator`.  The ``*args`` and ``**kwargs`` are the
        same as `~.ticker.LogLocator`.
        """
        self._colorbar = colorbar
        super().__init__(*args, **kwargs)

    def tick_values(self, vmin, vmax):
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        vmin = max(vmin, self._colorbar.norm.vmin)
        vmax = min(vmax, self._colorbar.norm.vmax)
        ticks = super().tick_values(vmin, vmax)
        rtol = (np.log10(vmax) - np.log10(vmin)) * 1e-10
        ticks = ticks[(np.log10(ticks) >= np.log10(vmin) - rtol) &
                      (np.log10(ticks) <= np.log10(vmax) + rtol)]
        return ticks
