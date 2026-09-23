    def set_x(self, x):
        """
        Set the *x* position of the text

        ACCEPTS: float
        """
        self._x = x
        self.stale = True
