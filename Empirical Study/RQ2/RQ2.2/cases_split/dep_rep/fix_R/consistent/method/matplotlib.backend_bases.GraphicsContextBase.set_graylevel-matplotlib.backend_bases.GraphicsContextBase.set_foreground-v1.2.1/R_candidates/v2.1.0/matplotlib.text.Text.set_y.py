    def set_y(self, y):
        """
        Set the *y* position of the text

        ACCEPTS: float
        """
        self._y = y
        self.stale = True
