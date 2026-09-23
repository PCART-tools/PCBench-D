    def set_width(self, width):
        """
        Set the width (thickness) of the annulus ring.

        The width is measured inwards from the outer ellipse.

        Parameters
        ----------
        width : float
        """
        if min(self.a, self.b) <= width:
            raise ValueError(
                'Width of annulus must be less than or equal semi-minor axis')

        self._width = width
        self._path = None
        self.stale = True
