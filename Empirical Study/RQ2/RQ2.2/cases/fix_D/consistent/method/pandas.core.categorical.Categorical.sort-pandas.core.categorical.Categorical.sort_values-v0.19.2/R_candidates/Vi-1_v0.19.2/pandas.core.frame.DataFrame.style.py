    @property
    def style(self):
        """
        Property returning a Styler object containing methods for
        building a styled HTML representation fo the DataFrame.

        See Also
        --------
        pandas.formats.style.Styler
        """
        from pandas.formats.style import Styler
        return Styler(self)
