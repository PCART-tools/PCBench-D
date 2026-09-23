    def tick_values(self, vmin, vmax):
        vmin = max(vmin, self._colorbar.norm.vmin)
        vmax = min(vmax, self._colorbar.norm.vmax)
        ticks = ticker.MaxNLocator.tick_values(self, vmin, vmax)
        return ticks[(ticks >= vmin) & (ticks <= vmax)]
