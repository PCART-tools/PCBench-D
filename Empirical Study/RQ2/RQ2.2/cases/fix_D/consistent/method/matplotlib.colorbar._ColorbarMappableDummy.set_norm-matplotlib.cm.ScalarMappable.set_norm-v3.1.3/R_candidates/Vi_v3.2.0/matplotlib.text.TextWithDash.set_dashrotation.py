    def set_dashrotation(self, dr):
        """
        Set the rotation of the dash, in degrees.

        Parameters
        ----------
        dr : float
        """
        self._dashrotation = dr
        self.stale = True
