    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target) -> tuple[np.ndarray, np.ndarray]:
        # both returned ndarrays are np.intp
        target = ibase.ensure_index(target)
        return self._get_indexer_non_unique(target._values)
