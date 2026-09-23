    @Substitution(name='groupby')
    def pad(self, limit=None):
        """
        Forward fill the values

        Parameters
        ----------
        limit : integer, optional
            limit of how many values to fill

        See Also
        --------
        Series.pad
        DataFrame.pad
        Series.fillna
        DataFrame.fillna
        """
        return self._fill('ffill', limit=limit)
