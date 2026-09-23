    def _get_value(self, index, col, takeable: bool = False) -> Scalar:
        """
        Quickly retrieve single value at passed column and index.

        Parameters
        ----------
        index : row label
        col : column label
        takeable : interpret the index/col as indexers, default False

        Returns
        -------
        scalar

        Notes
        -----
        Assumes that both `self.index._index_as_unique` and
        `self.columns._index_as_unique`; Caller is responsible for checking.
        """
        if takeable:
            series = self._ixs(col, axis=1)
            return series._values[index]

        series = self._get_item_cache(col)
        engine = self.index._engine

        if not isinstance(self.index, MultiIndex):
            # CategoricalIndex: Trying to use the engine fastpath may give incorrect
            #  results if our categories are integers that dont match our codes
            # IntervalIndex: IntervalTree has no get_loc
            row = self.index.get_loc(index)
            return series._values[row]

        # For MultiIndex going through engine effectively restricts us to
        #  same-length tuples; see test_get_set_value_no_partial_indexing
        loc = engine.get_loc(index)
        return series._values[loc]
