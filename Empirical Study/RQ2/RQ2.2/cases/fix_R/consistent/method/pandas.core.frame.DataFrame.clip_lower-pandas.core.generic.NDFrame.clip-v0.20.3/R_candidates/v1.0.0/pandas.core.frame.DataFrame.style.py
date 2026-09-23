    @property
    def style(self) -> "Styler":
        """
        Returns a Styler object.

        Contains methods for building a styled HTML representation of the DataFrame.
        a styled HTML representation fo the DataFrame.

        See Also
        --------
        io.formats.style.Styler
        """
        from pandas.io.formats.style import Styler

        return Styler(self)
