    def set_fontsize(self, size):
        """
        Set the fontsize of the cell text

        ACCEPTS: a float in points
        """

        for cell in six.itervalues(self._cells):
            cell.set_fontsize(size)
        self.stale = True
