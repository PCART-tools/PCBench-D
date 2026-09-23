    def set_edgecolor(self, color):
        """
        Set the patch edge color

        ACCEPTS: mpl color spec, None, 'none', or 'auto'
        """
        self._original_edgecolor = color
        self._set_edgecolor(color)
