    def __call__(self):
        vmin = self._colorbar.norm.vmin
        vmax = self._colorbar.norm.vmax
        ticks = ticker.AutoMinorLocator.__call__(self)
        rtol = (vmax - vmin) * 1e-10
        return ticks[(ticks >= vmin - rtol) & (ticks <= vmax + rtol)]
