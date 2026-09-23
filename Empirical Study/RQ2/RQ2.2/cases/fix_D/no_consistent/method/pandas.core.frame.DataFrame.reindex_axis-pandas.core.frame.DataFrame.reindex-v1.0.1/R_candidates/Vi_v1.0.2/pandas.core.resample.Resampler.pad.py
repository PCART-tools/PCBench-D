    def pad(self, limit=None):
        """
        Forward fill the values.

        Parameters
        ----------
        limit : int, optional
            Limit of how many values to fill.

        Returns
        -------
        An upsampled Series.

        See Also
        --------
        Series.fillna
        DataFrame.fillna
        """
        return self._upsample("pad", limit=limit)
