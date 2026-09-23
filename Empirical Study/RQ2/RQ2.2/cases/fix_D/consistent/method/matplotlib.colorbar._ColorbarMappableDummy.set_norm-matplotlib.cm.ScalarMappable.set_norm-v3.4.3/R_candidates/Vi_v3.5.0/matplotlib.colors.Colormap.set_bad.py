    def set_bad(self, color='k', alpha=None):
        """Set the color for masked values."""
        _warn_if_global_cmap_modified(self)
        self._rgba_bad = to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
