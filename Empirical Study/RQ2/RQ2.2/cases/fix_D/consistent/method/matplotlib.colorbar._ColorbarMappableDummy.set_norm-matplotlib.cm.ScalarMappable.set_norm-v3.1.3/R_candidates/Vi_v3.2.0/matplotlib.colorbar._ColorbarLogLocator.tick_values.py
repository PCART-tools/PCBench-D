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
