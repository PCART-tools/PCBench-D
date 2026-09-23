    def set_edgecolor(self, color):
        """
        Set the patch edge color.

        Parameters
        ----------
        color : :mpltype:`color` or None
        """
        self._original_edgecolor = color
        self._set_edgecolor(color)
