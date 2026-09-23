    def auto_set_font_size(self, value=True):
        """ Automatically set font size. """
        self._autoFontsize = value
        self.stale = True
