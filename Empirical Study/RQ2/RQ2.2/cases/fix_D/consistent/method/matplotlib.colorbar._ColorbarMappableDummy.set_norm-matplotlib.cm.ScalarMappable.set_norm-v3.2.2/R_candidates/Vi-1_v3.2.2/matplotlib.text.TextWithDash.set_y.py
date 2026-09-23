    def set_y(self, y):
        """
        Set the *y* position of the :class:`TextWithDash`.

        Parameters
        ----------
        y : float
        """
        self._dashy = float(y)
        self.stale = True
