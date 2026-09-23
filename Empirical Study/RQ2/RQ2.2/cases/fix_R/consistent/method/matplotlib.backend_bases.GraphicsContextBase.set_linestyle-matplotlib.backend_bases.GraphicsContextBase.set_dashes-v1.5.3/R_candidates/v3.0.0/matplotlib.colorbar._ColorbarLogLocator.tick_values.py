    def tick_values(self, vmin, vmax):
        vmin = self._colorbar.norm.vmin
        vmax = self._colorbar.norm.vmax
        ticks = ticker.LogLocator.tick_values(self, vmin, vmax)
        return ticks[(ticks >= vmin) & (ticks <= vmax)]
