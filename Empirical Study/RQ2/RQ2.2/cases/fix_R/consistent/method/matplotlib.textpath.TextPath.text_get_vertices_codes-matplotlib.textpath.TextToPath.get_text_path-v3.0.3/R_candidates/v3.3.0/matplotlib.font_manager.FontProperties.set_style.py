    def set_style(self, style):
        """
        Set the font style.  Values are: 'normal', 'italic' or 'oblique'.
        """
        if style is None:
            style = rcParams['font.style']
        cbook._check_in_list(['normal', 'italic', 'oblique'], style=style)
        self._slant = style
