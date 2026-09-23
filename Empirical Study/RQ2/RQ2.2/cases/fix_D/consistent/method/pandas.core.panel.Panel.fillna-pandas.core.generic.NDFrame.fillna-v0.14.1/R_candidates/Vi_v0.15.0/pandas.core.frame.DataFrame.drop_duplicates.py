    @deprecate_kwarg(old_arg_name='cols', new_arg_name='subset')
    def drop_duplicates(self, subset=None, take_last=False, inplace=False):
        """
        Return DataFrame with duplicate rows removed, optionally only
        considering certain columns

        Parameters
        ----------
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns
        take_last : boolean, default False
            Take the last observed row in a row. Defaults to the first row
        inplace : boolean, default False
            Whether to drop duplicates in place or to return a copy
        cols : kwargs only argument of subset [deprecated]

        Returns
        -------
        deduplicated : DataFrame
        """
        duplicated = self.duplicated(subset, take_last=take_last)

        if inplace:
            inds, = (-duplicated).nonzero()
            new_data = self._data.take(inds)
            self._update_inplace(new_data)
        else:
            return self[-duplicated]
