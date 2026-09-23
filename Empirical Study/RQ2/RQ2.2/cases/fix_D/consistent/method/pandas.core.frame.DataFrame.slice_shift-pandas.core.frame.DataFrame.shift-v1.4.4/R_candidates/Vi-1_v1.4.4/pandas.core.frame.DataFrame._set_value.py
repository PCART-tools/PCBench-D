    def _set_value(
        self, index: IndexLabel, col, value: Scalar, takeable: bool = False
    ) -> None:
        """
        Put single value at passed column and index.

        Parameters
        ----------
        index : Label
            row label
        col : Label
            column label
        value : scalar
        takeable : bool, default False
            Sets whether or not index/col interpreted as indexers
        """
        try:
            if takeable:
                series = self._ixs(col, axis=1)
                loc = index
            else:
                series = self._get_item_cache(col)
                loc = self.index.get_loc(index)

            # setitem_inplace will do validation that may raise TypeError
            #  or ValueError
            series._mgr.setitem_inplace(loc, value)

        except (KeyError, TypeError, ValueError):
            # set using a non-recursive method & reset the cache
            if takeable:
                self.iloc[index, col] = value
            else:
                self.loc[index, col] = value
            self._item_cache.pop(col, None)
