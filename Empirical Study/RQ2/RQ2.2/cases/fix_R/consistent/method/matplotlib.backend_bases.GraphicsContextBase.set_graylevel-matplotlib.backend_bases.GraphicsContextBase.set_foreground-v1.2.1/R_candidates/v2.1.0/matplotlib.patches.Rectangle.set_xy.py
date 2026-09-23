    def set_xy(self, xy):
        """
        Set the left and bottom coords of the rectangle

        ACCEPTS: 2-item sequence
        """
        self._x, self._y = xy
        self.stale = True
