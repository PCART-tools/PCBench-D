    def set_under(self, color='k', alpha=None):
        """
        Set the color for low out-of-range values when ``norm.clip = False``.
        """
        _warn_if_global_cmap_modified(self)
        self._rgba_under = to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
