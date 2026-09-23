    def set_bad(self, color='k', alpha=None):
        """Set color to be used for masked values.
        """
        self._rgba_bad = colorConverter.to_rgba(color, alpha)
        if self._isinit:
            self._set_extremes()
