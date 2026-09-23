    @Appender(_index_shared_docs['_convert_arr_indexer'])
    def _convert_arr_indexer(self, keyarr):
        # Cast the indexer to uint64 if possible so
        # that the values returned from indexing are
        # also uint64.
        keyarr = _asarray_tuplesafe(keyarr)
        if is_integer_dtype(keyarr):
            return _asarray_tuplesafe(keyarr, dtype=np.uint64)
        return keyarr
