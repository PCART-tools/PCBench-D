    @doc(Index._convert_arr_indexer)
    def _convert_arr_indexer(self, keyarr):
        # Cast the indexer to uint64 if possible so that the values returned
        # from indexing are also uint64.
        dtype = None
        if is_integer_dtype(keyarr) or (
            lib.infer_dtype(keyarr, skipna=False) == "integer"
        ):
            dtype = np.uint64

        return com.asarray_tuplesafe(keyarr, dtype=dtype)
