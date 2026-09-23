    @Appender(_index_shared_docs["_convert_index_indexer"])
    def _convert_index_indexer(self, keyarr):
        return self._shallow_copy(keyarr)
