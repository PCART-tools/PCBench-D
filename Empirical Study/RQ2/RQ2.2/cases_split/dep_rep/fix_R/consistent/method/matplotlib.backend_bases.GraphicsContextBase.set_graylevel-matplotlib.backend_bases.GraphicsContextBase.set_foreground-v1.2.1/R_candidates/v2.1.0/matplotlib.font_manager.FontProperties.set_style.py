    def set_style(self, style):
        """
        Set the font style.  Values are: 'normal', 'italic' or
        'oblique'.
        """
        if style is None:
            style = rcParams['font.style']
        if style not in ('normal', 'italic', 'oblique'):
            raise ValueError("style must be normal, italic or oblique")
        self._slant = style
