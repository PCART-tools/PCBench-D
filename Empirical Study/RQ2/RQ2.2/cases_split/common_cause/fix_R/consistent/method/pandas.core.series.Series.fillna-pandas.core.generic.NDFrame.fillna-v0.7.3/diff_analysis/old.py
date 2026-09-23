    def fillna(self, value=None, method='pad', inplace=False):
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

        See also
        --------
        reindex, asfreq

        Returns
        -------
        filled : Series
        """
        mask = isnull(self.values)

        if value is not None:
            result = self.copy() if not inplace else self
            np.putmask(result, mask, value)
        else:
            if method is None:  # pragma: no cover
                raise ValueError('must specify a fill method')

            method = com._clean_fill_method(method)

            # sadness. for Python 2.5 compatibility
            mask = mask.astype(np.uint8)

            if method == 'pad':
                indexer = lib.get_pad_indexer(mask)
            elif method == 'backfill':
                indexer = lib.get_backfill_indexer(mask)

            if inplace:
                self.values[:] = self.values.take(indexer)
                result = self
            else:
                new_values = self.values.take(indexer)
                result = Series(new_values, index=self.index, name=self.name)

        return result
