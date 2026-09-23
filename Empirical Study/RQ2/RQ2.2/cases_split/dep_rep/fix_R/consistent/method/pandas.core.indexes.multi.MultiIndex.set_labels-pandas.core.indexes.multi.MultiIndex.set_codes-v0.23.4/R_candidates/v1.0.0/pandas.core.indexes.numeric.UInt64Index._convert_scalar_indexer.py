    @Appender(_index_shared_docs["_convert_scalar_indexer"])
    def _convert_scalar_indexer(self, key, kind=None):
        assert kind in ["ix", "loc", "getitem", "iloc", None]

        # don't coerce ilocs to integers
        if kind != "iloc":
            key = self._maybe_cast_indexer(key)
        return super()._convert_scalar_indexer(key, kind=kind)
