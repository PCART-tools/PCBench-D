    @cache_readonly
    def indices(self):
        # we have a list of groupers
        if isinstance(self.grouper, BaseGrouper):
            return self.grouper.indices

        values = _ensure_categorical(self.grouper)
        return values._reverse_indexer()
