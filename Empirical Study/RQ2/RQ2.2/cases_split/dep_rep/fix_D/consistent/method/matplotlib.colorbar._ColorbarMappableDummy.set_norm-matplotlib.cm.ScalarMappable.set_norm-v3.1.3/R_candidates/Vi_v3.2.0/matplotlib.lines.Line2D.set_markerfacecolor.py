    def set_markerfacecolor(self, fc):
        """
        Set the marker face color.

        Parameters
        ----------
        fc : color
        """
        if fc is None:
            fc = 'auto'
        if np.any(self._markerfacecolor != fc):
            self.stale = True
        self._markerfacecolor = fc
