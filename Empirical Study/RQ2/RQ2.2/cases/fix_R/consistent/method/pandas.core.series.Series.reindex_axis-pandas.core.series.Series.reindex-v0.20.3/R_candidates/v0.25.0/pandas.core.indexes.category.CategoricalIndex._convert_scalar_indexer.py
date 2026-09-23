    @Appender(_index_shared_docs["_convert_scalar_indexer"])
    def _convert_scalar_indexer(self, key, kind=None):
        if self.categories._defer_to_indexing:
            return self.categories._convert_scalar_indexer(key, kind=kind)

        return super()._convert_scalar_indexer(key, kind=kind)
