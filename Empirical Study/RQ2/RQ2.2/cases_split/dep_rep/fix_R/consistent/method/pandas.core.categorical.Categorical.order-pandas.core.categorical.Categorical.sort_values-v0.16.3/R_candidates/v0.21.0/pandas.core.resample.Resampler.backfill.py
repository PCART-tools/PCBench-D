    def backfill(self, limit=None):
        """
        Backward fill the values

        Parameters
        ----------
        limit : integer, optional
            limit of how many values to fill

        Returns
        -------
        an upsampled Series

        See Also
        --------
        Series.fillna
        DataFrame.fillna
        """
        return self._upsample('backfill', limit=limit)
