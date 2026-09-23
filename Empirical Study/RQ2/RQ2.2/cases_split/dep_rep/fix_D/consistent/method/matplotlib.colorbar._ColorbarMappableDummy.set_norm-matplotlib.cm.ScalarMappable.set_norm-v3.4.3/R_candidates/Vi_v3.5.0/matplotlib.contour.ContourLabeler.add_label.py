    def add_label(self, x, y, rotation, lev, cvalue):
        """
        Add contour label using :class:`~matplotlib.text.Text` class.
        """
        t = self._get_label_text(x, y, rotation)
        self._add_label(t, x, y, lev, cvalue)
