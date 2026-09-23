    def nearest(self, limit=None):
        """
        Fill values with nearest neighbor starting from center

        Parameters
        ----------
        limit : integer, optional
            limit of how many values to fill

            .. versionadded:: 0.21.0

        Returns
        -------
        an upsampled Series

        See Also
        --------
        Series.fillna
        DataFrame.fillna
        """
        return self._upsample('nearest', limit=limit)
