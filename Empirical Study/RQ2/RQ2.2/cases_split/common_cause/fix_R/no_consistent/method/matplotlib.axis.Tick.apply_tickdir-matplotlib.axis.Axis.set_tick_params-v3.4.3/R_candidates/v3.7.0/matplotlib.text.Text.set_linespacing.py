    def set_linespacing(self, spacing):
        """
        Set the line spacing as a multiple of the font size.

        The default line spacing is 1.2.

        Parameters
        ----------
        spacing : float (multiple of font size)
        """
        _api.check_isinstance(Real, spacing=spacing)
        self._linespacing = spacing
        self.stale = True
