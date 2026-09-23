    @Appender(_index_shared_docs["_convert_scalar_indexer"])
    def _convert_scalar_indexer(self, key, kind=None):
        if kind == "iloc":
            return super()._convert_scalar_indexer(key, kind=kind)
        return key
