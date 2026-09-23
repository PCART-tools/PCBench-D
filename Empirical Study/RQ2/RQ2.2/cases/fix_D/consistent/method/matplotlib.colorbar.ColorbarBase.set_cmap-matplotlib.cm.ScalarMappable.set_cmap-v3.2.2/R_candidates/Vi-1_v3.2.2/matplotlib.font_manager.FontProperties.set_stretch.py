    def set_stretch(self, stretch):
        """
        Set the font stretch or width.  Options are: 'ultra-condensed',
        'extra-condensed', 'condensed', 'semi-condensed', 'normal',
        'semi-expanded', 'expanded', 'extra-expanded' or
        'ultra-expanded', or a numeric value in the range 0-1000.
        """
        if stretch is None:
            stretch = rcParams['font.stretch']
        try:
            stretch = int(stretch)
            if stretch < 0 or stretch > 1000:
                raise ValueError()
        except ValueError:
            if stretch not in stretch_dict:
                raise ValueError("stretch is invalid")
        self._stretch = stretch
