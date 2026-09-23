    @cache_readonly
    def indices(self):
        values = _ensure_categorical(self.grouper)
        return values._reverse_indexer()
