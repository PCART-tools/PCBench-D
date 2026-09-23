    @property
    def viewLim(self):
        self._unstale_viewLim()
        return self._viewLim
