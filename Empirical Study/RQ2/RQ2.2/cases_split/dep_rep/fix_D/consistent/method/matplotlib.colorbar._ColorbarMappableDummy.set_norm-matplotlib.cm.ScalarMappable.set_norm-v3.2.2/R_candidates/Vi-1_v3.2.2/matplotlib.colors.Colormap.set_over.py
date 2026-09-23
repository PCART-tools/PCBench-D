    def set_over(self, color='k', alpha=None):
        """
        Set the color for high out-of-range values when ``norm.clip = False``.
        """
        self._rgba_over = to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
