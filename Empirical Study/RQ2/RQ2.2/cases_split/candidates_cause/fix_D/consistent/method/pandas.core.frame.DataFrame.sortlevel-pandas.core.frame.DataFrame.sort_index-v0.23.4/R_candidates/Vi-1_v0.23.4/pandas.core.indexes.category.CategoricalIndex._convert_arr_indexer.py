    @Appender(_index_shared_docs['_convert_arr_indexer'])
    def _convert_arr_indexer(self, keyarr):
        keyarr = com._asarray_tuplesafe(keyarr)

        if self.categories._defer_to_indexing:
            return keyarr

        return self._shallow_copy(keyarr)
