    @Appender(_index_shared_docs['_convert_arr_indexer'])
    def _convert_arr_indexer(self, keyarr):
        keyarr = _asarray_tuplesafe(keyarr)
        return keyarr
