    def fillna(self, method, limit=None):
        """
        Fill missing values

        Parameters
        ----------
        method : str, method of resampling ('ffill', 'bfill')
        limit : integer, optional
            limit of how many values to fill

        See Also
        --------
        Series.fillna
        DataFrame.fillna
        """
        return self._upsample(method, limit=limit)
