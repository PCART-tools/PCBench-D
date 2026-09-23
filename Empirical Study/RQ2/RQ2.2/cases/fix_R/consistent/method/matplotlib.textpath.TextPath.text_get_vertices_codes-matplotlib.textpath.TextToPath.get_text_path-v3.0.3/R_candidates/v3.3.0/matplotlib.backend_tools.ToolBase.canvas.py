    @property
    def canvas(self):
        if not self._figure:
            return None
        return self._figure.canvas
