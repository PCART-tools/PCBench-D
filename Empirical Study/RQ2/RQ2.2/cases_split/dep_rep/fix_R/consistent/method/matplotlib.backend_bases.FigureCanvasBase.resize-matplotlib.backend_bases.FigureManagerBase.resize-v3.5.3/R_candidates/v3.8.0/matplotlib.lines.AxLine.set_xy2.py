    def set_xy2(self, x, y):
        """
        Set the *xy2* value of the line.

        Parameters
        ----------
        x, y : float
            Points for the line to pass through.
        """
        if self._slope is None:
            self._xy2 = x, y
        else:
            raise ValueError("Cannot set an 'xy2' value while 'slope' is set;"
                             " they differ but their functionalities overlap")
