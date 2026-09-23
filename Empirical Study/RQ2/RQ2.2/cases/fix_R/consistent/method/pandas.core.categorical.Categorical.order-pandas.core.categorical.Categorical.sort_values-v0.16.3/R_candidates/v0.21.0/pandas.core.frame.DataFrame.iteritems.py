    def iteritems(self):
        """
        Iterator over (column name, Series) pairs.

        See also
        --------
        iterrows : Iterate over DataFrame rows as (index, Series) pairs.
        itertuples : Iterate over DataFrame rows as namedtuples of the values.

        """
        if self.columns.is_unique and hasattr(self, '_item_cache'):
            for k in self.columns:
                yield k, self._get_item_cache(k)
        else:
            for i, k in enumerate(self.columns):
                yield k, self._ixs(i, axis=1)
