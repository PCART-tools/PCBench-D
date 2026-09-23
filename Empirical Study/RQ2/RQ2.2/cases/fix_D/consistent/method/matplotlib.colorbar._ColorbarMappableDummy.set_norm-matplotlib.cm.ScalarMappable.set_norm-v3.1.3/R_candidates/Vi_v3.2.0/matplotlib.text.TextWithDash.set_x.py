    def set_x(self, x):
        """
        Set the *x* position of the :class:`TextWithDash`.

        Parameters
        ----------
        x : float
        """
        self._dashx = float(x)
        self.stale = True
