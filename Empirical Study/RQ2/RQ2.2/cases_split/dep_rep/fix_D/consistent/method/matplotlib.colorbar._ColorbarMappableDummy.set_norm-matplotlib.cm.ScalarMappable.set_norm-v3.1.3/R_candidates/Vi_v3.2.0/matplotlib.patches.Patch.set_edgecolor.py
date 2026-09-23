    def set_edgecolor(self, color):
        """
        Set the patch edge color.

        Parameters
        ----------
        color : color or None or 'auto'
        """
        self._original_edgecolor = color
        self._set_edgecolor(color)
