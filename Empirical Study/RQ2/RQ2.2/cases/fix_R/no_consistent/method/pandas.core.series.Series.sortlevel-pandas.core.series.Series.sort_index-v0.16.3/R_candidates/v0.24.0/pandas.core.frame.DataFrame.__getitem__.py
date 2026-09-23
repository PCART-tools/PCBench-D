    def __getitem__(self, key):
        key = com.apply_if_callable(key, self)

        # shortcut if the key is in columns
        try:
            if self.columns.is_unique and key in self.columns:
                if self.columns.nlevels > 1:
                    return self._getitem_multilevel(key)
                return self._get_item_cache(key)
        except (TypeError, ValueError):
            # The TypeError correctly catches non hashable "key" (e.g. list)
            # The ValueError can be removed once GH #21729 is fixed
            pass

        # Do we have a slicer (on rows)?
        indexer = convert_to_index_sliceable(self, key)
        if indexer is not None:
            return self._slice(indexer, axis=0)

        # Do we have a (boolean) DataFrame?
        if isinstance(key, DataFrame):
            return self._getitem_frame(key)

        # Do we have a (boolean) 1d indexer?
        if com.is_bool_indexer(key):
            return self._getitem_bool_array(key)

        # We are left with two options: a single key, and a collection of keys,
        # We interpret tuples as collections only for non-MultiIndex
        is_single_key = isinstance(key, tuple) or not is_list_like(key)

        if is_single_key:
            if self.columns.nlevels > 1:
                return self._getitem_multilevel(key)
            indexer = self.columns.get_loc(key)
            if is_integer(indexer):
                indexer = [indexer]
        else:
            if is_iterator(key):
                key = list(key)
            indexer = self.loc._convert_to_indexer(key, axis=1,
                                                   raise_missing=True)

        # take() does not accept boolean indexers
        if getattr(indexer, "dtype", None) == bool:
            indexer = np.where(indexer)[0]

        data = self._take(indexer, axis=1)

        if is_single_key:
            # What does looking for a single key in a non-unique index return?
            # The behavior is inconsistent. It returns a Series, except when
            # - the key itself is repeated (test on data.shape, #9519), or
            # - we have a MultiIndex on columns (test on self.columns, #21309)
            if data.shape[1] == 1 and not isinstance(self.columns, MultiIndex):
                data = data[key]

        return data
