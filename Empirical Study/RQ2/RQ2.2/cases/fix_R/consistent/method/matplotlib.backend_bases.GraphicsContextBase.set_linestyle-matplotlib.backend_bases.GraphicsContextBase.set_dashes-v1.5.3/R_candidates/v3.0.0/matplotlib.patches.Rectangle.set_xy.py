    def set_xy(self, xy):
        """
        Set the left and bottom coords of the rectangle.

        Parameters
        ----------
        xy : 2-item sequence
        """
        self._x0, self._y0 = xy
        self._update_x1()
        self._update_y1()
        self.stale = True
