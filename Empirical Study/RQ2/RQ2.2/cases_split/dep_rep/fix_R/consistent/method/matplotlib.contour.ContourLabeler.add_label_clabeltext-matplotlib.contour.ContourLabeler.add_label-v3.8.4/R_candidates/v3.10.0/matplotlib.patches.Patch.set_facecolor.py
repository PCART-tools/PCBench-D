    def set_facecolor(self, color):
        """
        Set the patch face color.

        Parameters
        ----------
        color : :mpltype:`color` or None
        """
        self._original_facecolor = color
        self._set_facecolor(color)
