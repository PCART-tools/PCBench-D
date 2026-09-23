    def tick_values(self, vmin, vmax):
        if vmax < vmin:
            vmin, vmax = vmax, vmin
        vmin = self._base.ge(vmin)
        base = self._base.get_base()
        n = (vmax - vmin + 0.001 * base) // base
        locs = vmin - base + np.arange(n + 3) * base
        return self.raise_if_exceeds(locs)
