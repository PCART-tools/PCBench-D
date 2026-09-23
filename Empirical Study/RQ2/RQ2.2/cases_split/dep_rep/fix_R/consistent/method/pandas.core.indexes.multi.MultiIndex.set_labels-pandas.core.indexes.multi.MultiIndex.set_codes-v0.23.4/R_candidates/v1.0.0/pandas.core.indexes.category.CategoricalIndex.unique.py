    @Appender(_index_shared_docs["index_unique"] % _index_doc_kwargs)
    def unique(self, level=None):
        if level is not None:
            self._validate_index_level(level)
        result = self.values.unique()
        # CategoricalIndex._shallow_copy keeps original dtype
        # if not otherwise specified
        return self._shallow_copy(result, dtype=result.dtype)
