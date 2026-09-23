    def set_linespacing(self, spacing):
        """
        Set the line spacing as a multiple of the font size.
        Default is 1.2.

        ACCEPTS: float (multiple of font size)
        """
        self._linespacing = spacing
        self.stale = True
