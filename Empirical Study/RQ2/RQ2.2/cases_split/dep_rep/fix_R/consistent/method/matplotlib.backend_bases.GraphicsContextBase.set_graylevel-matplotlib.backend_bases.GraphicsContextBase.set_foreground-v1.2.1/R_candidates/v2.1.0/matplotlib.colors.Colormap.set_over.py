    def set_over(self, color='k', alpha=None):
        """Set color to be used for high out-of-range values.
           Requires norm.clip = False
        """
        self._rgba_over = colorConverter.to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
