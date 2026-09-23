    @Appender(_index_shared_docs["_convert_arr_indexer"])
    def _convert_arr_indexer(self, keyarr):
        keyarr = com.asarray_tuplesafe(keyarr)
        return keyarr
