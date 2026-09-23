    @Appender(_index_shared_docs['_convert_index_indexer'])
    def _convert_index_indexer(self, keyarr):
        # Cast the indexer to uint64 if possible so
        # that the values returned from indexing are
        # also uint64.
        if keyarr.is_integer():
            return keyarr.astype(np.uint64)
        return keyarr
