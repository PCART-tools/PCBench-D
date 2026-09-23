    def set_dashlength(self, dl):
        """
        Set the length of the dash, in canvas units.

        Parameters
        ----------
        dl : float
        """
        self._dashlength = dl
        self.stale = True
