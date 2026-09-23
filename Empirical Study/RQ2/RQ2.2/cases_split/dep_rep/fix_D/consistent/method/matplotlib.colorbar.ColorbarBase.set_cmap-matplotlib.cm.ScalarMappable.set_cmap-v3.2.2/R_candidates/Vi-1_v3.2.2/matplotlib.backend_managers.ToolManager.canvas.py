    @property
    def canvas(self):
        """Canvas managed by FigureManager."""
        if not self._figure:
            return None
        return self._figure.canvas
