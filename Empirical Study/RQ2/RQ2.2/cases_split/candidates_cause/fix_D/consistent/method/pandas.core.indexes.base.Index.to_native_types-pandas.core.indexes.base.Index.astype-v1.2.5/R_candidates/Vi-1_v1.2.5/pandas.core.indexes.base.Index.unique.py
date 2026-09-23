    def unique(self, level=None):
        """
        Return unique values in the index.

        Unique values are returned in order of appearance, this does NOT sort.

        Parameters
        ----------
        level : int or str, optional, default None
            Only return values from specified level (for MultiIndex).

        Returns
        -------
        Index without duplicates

        See Also
        --------
        unique : Numpy array of unique values in that column.
        Series.unique : Return unique values of Series object.
        """
        if level is not None:
            self._validate_index_level(level)

        if self.is_unique:
            return self._shallow_copy()

        result = super().unique()
        return self._shallow_copy(result)
