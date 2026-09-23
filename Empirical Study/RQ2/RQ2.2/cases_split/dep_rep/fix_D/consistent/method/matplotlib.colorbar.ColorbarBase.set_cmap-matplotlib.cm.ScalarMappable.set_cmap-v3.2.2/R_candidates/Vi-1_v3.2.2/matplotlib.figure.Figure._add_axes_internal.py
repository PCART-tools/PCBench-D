    def _add_axes_internal(self, key, ax):
        """Private helper for `add_axes` and `add_subplot`."""
        self._axstack.add(key, ax)
        self.sca(ax)
        ax._remove_method = self._remove_ax
        self.stale = True
        ax.stale_callback = _stale_figure_callback
        return ax
