
    def fillna(self, value=None, method=None, inplace=False,
               limit=None):
        """
        Fill NA/NaN values using the specified method

        Parameters
        ----------
        value : any kind (should be same type as array)
            Value to use to fill holes (e.g. 0)
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default 'pad'
            Method to use for filling holes in reindexed Series
            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap
        inplace : boolean, default False
            If True, fill the Series in place. Note: this will modify any other
            views on this Series, for example a column in a DataFrame. Returns
            a reference to the filled object, which is self if inplace=True
        limit : int, default None
            Maximum size gap to forward or backward fill

        See also
        --------
        reindex, asfreq

        Returns
        -------
        filled : Series
        """
        if not self._can_hold_na:
            return self.copy() if not inplace else None

        if value is not None:
            if method is not None:
                raise ValueError('Cannot specify both a fill value and method')
            result = self.copy() if not inplace else self
            mask = isnull(self.values)
            np.putmask(result, mask, value)
        else:
            if method is None:  # pragma: no cover
                raise ValueError('must specify a fill method or value')

            fill_f = _get_fill_func(method)

            if inplace:
                values = self.values
            else:
                values = self.values.copy()

            fill_f(values, limit=limit)

            if inplace:
                result = self
            else:
                result = Series(values, index=self.index, name=self.name)

        if not inplace:
            return result
