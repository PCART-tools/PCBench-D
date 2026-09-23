    def set_x(self, x):
        """
        Set the *x* position of the :class:`TextWithDash`.

        ACCEPTS: float
        """
        self._dashx = float(x)
        self.stale = True
