    def set_markerfacecolor(self, fc):
        """
        Set the marker face color.

        Parameters
        ----------
        fc : :mpltype:`color`
        """
        self._set_markercolor("markerfacecolor", True, fc)
