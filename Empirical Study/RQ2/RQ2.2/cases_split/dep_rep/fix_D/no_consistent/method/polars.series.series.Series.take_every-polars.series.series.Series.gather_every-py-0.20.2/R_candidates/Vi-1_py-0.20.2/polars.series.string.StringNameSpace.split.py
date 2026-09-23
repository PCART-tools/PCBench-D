    def split(self, by: IntoExpr, *, inclusive: bool = False) -> Series:
        """
        Split the string by a substring.

        Parameters
        ----------
        by
            Substring to split by.
        inclusive
            If True, include the split character/string in the results.

        Returns
        -------
        Series
            Series of data type `List(Utf8)`.

        """
