    @property
    def style(self) -> Styler:
        """
        Returns a Styler object.

        Contains methods for building a styled HTML representation of the DataFrame.

        See Also
        --------
        io.formats.style.Styler : Helps style a DataFrame or Series according to the
            data with HTML and CSS.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2, 3]})
        >>> df.style  # doctest: +SKIP

        Please see
        `Table Visualization <../../user_guide/style.ipynb>`_ for more examples.
        """
        from pandas.io.formats.style import Styler

        return Styler(self)
