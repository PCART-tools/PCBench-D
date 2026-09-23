    def isna(self):
        """
        Detect missing values

        .. versionadded:: 0.20.0

        Returns
        -------
        a boolean array of whether my values are NA

        See also
        --------
        isnull : alias of isna
        pandas.isna : top-level isna
        """
        return self._isnan
