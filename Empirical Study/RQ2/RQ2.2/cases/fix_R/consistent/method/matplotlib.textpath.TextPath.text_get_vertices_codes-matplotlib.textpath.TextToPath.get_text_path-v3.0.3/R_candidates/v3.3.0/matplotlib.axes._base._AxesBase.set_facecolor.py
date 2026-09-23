    def set_facecolor(self, color):
        """
        Set the facecolor of the Axes.

        Parameters
        ----------
        color : color
        """
        self._facecolor = color
        self.stale = True
        return self.patch.set_facecolor(color)
