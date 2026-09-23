    @Appender(_index_shared_docs["_convert_scalar_indexer"])
    def _convert_scalar_indexer(self, key, kind=None):
        assert kind in ["ix", "loc", "getitem", "iloc", None]

        if kind == "iloc":
            return self._validate_indexer("positional", key, kind)

        return key
