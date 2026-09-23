    def set_facecolor(self, color):
        """
        Set the patch face color

        ACCEPTS: mpl color spec, or None for default, or 'none' for no color
        """
        self._original_facecolor = color
        self._set_facecolor(color)
