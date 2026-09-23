    def set_dashrotation(self, dr):
        """
        Set the rotation of the dash, in degrees

        ACCEPTS: float (degrees)
        """
        self._dashrotation = dr
        self.stale = True
