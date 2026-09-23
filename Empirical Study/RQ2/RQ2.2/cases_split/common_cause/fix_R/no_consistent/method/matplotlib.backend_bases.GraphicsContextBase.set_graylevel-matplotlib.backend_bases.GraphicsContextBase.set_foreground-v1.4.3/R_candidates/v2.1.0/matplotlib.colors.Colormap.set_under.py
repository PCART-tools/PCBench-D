    def set_under(self, color='k', alpha=None):
        """Set color to be used for low out-of-range values.
           Requires norm.clip = False
        """
        self._rgba_under = colorConverter.to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
