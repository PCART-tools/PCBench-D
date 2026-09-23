    def notna(self):
        """
        Inverse of isna

        .. versionadded:: 0.20.0

        Returns
        -------
        a boolean array of whether my values are not NA

        See also
        --------
        notnull : alias of notna
        pandas.notna : top-level notna
        """
        return ~self.isna()
