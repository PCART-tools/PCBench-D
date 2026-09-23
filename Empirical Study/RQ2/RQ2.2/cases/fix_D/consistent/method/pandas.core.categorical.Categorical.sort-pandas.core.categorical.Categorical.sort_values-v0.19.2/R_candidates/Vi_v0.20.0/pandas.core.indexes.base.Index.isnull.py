    def isnull(self):
        """
        Detect missing values

        .. versionadded:: 0.20.0

        Returns
        -------
        a boolean array of whether my values are null

        See also
        --------
        pandas.isnull : pandas version
        """
        return self._isnan
