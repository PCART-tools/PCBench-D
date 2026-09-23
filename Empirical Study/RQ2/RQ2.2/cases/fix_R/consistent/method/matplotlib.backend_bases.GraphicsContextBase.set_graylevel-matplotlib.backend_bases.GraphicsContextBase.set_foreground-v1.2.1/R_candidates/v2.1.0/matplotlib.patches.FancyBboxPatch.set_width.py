    def set_width(self, w):
        """
        Set the width rectangle

        ACCEPTS: float
        """
        self._width = w
        self.stale = True
