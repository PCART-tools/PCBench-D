    def _get_indexer_strict(
        self, key, axis_name: str
    ) -> tuple[Index, npt.NDArray[np.intp]]:

        keyarr = key
        if not isinstance(keyarr, Index):
            keyarr = com.asarray_tuplesafe(keyarr)

        if len(keyarr) and not isinstance(keyarr[0], tuple):
            indexer = self._get_indexer_level_0(keyarr)

            self._raise_if_missing(key, indexer, axis_name)
            return self[indexer], indexer

        return super()._get_indexer_strict(key, axis_name)
