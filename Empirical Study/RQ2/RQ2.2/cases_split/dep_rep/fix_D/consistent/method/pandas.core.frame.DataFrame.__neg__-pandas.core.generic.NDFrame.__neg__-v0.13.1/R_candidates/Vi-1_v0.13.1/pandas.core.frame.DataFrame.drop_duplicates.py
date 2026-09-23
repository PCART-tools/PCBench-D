    def drop_duplicates(self, cols=None, take_last=False, inplace=False):
        """
        Return DataFrame with duplicate rows removed, optionally only
        considering certain columns

        Parameters
        ----------
        cols : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns
        take_last : boolean, default False
            Take the last observed row in a row. Defaults to the first row
        inplace : boolean, default False
            Whether to drop duplicates in place or to return a copy

        Returns
        -------
        deduplicated : DataFrame
        """

        duplicated = self.duplicated(cols, take_last=take_last)

        if inplace:
            inds, = (-duplicated).nonzero()
            new_data = self._data.take(inds)
            self._update_inplace(new_data)
        else:
            return self[-duplicated]
