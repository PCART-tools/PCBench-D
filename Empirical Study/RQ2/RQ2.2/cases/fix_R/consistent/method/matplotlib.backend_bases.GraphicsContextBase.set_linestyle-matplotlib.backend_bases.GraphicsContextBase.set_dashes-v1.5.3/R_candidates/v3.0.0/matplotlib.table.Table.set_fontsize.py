    def set_fontsize(self, size):
        """
        Set the font size, in points, of the cell text.

        Parameters
        ----------
        size : float
        """

        for cell in self._cells.values():
            cell.set_fontsize(size)
        self.stale = True
