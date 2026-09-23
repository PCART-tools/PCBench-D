    @Appender(_index_shared_docs["_convert_scalar_indexer"])
    def _convert_scalar_indexer(self, key, kind=None):
        if kind == "loc":
            try:
                return self.categories._convert_scalar_indexer(key, kind=kind)
            except TypeError:
                self._invalid_indexer("label", key)
        return super()._convert_scalar_indexer(key, kind=kind)
