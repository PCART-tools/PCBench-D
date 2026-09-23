    def set_x(self, x):
        """
        Set the left coord of the rectangle

        ACCEPTS: float
        """
        self._x = x
        self.stale = True
