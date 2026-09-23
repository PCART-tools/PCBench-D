    def notnull(self):
        """
        Reverse of isnull

        .. versionadded:: 0.20.0

        Returns
        -------
        a boolean array of whether my values are not null

        See also
        --------
        pandas.notnull : pandas version
        """
        return ~self.isnull()
