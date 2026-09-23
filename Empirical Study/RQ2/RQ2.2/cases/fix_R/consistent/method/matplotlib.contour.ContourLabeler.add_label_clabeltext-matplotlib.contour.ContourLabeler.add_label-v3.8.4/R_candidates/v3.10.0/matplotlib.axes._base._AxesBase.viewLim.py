    @property
    def viewLim(self):
        """The view limits as `.Bbox` in data coordinates."""
        self._unstale_viewLim()
        return self._viewLim
