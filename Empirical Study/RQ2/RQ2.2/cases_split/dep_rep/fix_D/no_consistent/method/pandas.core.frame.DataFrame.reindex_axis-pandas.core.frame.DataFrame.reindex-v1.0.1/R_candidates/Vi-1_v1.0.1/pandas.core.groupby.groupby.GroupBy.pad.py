    @Substitution(name="groupby")
    def pad(self, limit=None):
        """
        Forward fill the values.

        Parameters
        ----------
        limit : int, optional
            Limit of how many values to fill.

        Returns
        -------
        Series or DataFrame
            Object with missing values filled.

        See Also
        --------
        Series.pad
        DataFrame.pad
        Series.fillna
        DataFrame.fillna
        """
        return self._fill("ffill", limit=limit)
