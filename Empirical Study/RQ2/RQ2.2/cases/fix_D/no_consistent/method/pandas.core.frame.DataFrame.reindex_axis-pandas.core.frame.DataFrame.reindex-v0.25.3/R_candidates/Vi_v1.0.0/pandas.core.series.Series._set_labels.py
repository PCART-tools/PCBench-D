    def _set_labels(self, key, value):
        key = com.asarray_tuplesafe(key)
        indexer = self.index.get_indexer(key)
        mask = indexer == -1
        if mask.any():
            raise ValueError(f"{key[mask]} not contained in the index")
        self._set_values(indexer, value)
