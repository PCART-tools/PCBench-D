    def __getitem__(self, key):
        check_deprecated_indexers(key)
        key = lib.item_from_zerodim(key)
        key = com.apply_if_callable(key, self)

        if is_hashable(key) and not is_iterator(key):
            # is_iterator to exclude generator e.g. test_getitem_listlike
            # shortcut if the key is in columns
            is_mi = isinstance(self.columns, MultiIndex)
            # GH#45316 Return view if key is not duplicated
            # Only use drop_duplicates with duplicates for performance
            if not is_mi and (
                self.columns.is_unique
                and key in self.columns
                or key in self.columns.drop_duplicates(keep=False)
            ):
                return self._get_item_cache(key)

            elif is_mi and self.columns.is_unique and key in self.columns:
                return self._getitem_multilevel(key)
        # Do we have a slicer (on rows)?
        indexer = convert_to_index_sliceable(self, key)
        if indexer is not None:
            if isinstance(indexer, np.ndarray):
                indexer = lib.maybe_indices_to_slice(
                    indexer.astype(np.intp, copy=False), len(self)
                )
                if isinstance(indexer, np.ndarray):
                    # GH#43223 If we can not convert, use take
                    return self.take(indexer, axis=0)
            # either we have a slice or we have a string that can be converted
            #  to a slice for partial-string date indexing
            return self._slice(indexer, axis=0)

        # Do we have a (boolean) DataFrame?
        if isinstance(key, DataFrame):
            return self.where(key)

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
            indexer = self.columns._get_indexer_strict(key, "columns")[1]

        # take() does not accept boolean indexers
        if getattr(indexer, "dtype", None) == bool:
            indexer = np.where(indexer)[0]

        data = self._take_with_is_copy(indexer, axis=1)

        if is_single_key:
            # What does looking for a single key in a non-unique index return?
            # The behavior is inconsistent. It returns a Series, except when
            # - the key itself is repeated (test on data.shape, #9519), or
            # - we have a MultiIndex on columns (test on self.columns, #21309)
            if data.shape[1] == 1 and not isinstance(self.columns, MultiIndex):
                # GH#26490 using data[key] can cause RecursionError
                return data._get_item_cache(key)

        return data
