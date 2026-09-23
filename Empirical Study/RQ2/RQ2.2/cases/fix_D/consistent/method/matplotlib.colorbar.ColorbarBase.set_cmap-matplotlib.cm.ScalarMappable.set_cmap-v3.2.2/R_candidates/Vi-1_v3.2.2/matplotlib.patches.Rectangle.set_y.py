    def set_y(self, y):
        """Set the bottom coordinate of the rectangle."""
        self._y0 = y
        self._update_y1()
        self.stale = True
