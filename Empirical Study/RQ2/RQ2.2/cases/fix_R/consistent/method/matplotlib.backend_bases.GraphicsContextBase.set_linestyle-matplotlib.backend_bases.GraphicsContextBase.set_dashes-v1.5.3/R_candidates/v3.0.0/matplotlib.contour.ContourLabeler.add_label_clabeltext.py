    def add_label_clabeltext(self, x, y, rotation, lev, cvalue):
        """
        Add contour label using :class:`ClabelText` class.
        """
        # x, y, rotation is given in pixel coordinate. Convert them to
        # the data coordinate and create a label using ClabelText
        # class. This way, the roation of the clabel is along the
        # contour line always.

        t = self._get_label_clabeltext(x, y, rotation)
        self._add_label(t, x, y, lev, cvalue)
