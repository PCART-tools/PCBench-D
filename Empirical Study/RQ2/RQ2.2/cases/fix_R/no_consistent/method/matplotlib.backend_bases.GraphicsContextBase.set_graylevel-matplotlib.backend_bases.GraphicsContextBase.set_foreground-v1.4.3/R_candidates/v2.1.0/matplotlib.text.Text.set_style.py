    def set_style(self, fontstyle):
        """
        Set the font style.

        ACCEPTS: [ 'normal' | 'italic' | 'oblique']
        """
        self._fontproperties.set_style(fontstyle)
        self.stale = True
