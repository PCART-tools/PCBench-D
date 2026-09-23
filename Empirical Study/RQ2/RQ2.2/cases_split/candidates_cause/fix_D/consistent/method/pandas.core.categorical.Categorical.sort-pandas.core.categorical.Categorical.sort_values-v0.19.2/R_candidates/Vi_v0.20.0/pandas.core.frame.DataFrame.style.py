    @property
    def style(self):
        """
        Property returning a Styler object containing methods for
        building a styled HTML representation fo the DataFrame.

        See Also
        --------
        pandas.io.formats.style.Styler
        """
        from pandas.io.formats.style import Styler
        return Styler(self)
