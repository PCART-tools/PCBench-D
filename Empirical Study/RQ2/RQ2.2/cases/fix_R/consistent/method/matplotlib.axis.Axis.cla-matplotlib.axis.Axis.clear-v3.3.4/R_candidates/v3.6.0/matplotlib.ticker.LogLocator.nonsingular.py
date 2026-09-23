    def nonsingular(self, vmin, vmax):
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        if not np.isfinite(vmin) or not np.isfinite(vmax):
            vmin, vmax = 1, 10  # Initial range, no data plotted yet.
        elif vmax <= 0:
            _api.warn_external(
                "Data has no positive values, and therefore cannot be "
                "log-scaled.")
            vmin, vmax = 1, 10
        else:
            minpos = self.axis.get_minpos()
            if not np.isfinite(minpos):
                minpos = 1e-300  # This should never take effect.
            if vmin <= 0:
                vmin = minpos
            if vmin == vmax:
                vmin = _decade_less(vmin, self._base)
                vmax = _decade_greater(vmax, self._base)
        return vmin, vmax
