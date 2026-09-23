    def set_dashlength(self, dl):
        """
        Set the length of the dash.

        ACCEPTS: float (canvas units)
        """
        self._dashlength = dl
        self.stale = True
