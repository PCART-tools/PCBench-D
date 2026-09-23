    def tick_values(self, vmin, vmax):
        # flip if needed:
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        vmin = max(vmin, self._colorbar.norm.vmin)
        vmax = min(vmax, self._colorbar.norm.vmax)
        ticks = super().tick_values(vmin, vmax)
        rtol = (vmax - vmin) * 1e-10
        return ticks[(ticks >= vmin - rtol) & (ticks <= vmax + rtol)]
