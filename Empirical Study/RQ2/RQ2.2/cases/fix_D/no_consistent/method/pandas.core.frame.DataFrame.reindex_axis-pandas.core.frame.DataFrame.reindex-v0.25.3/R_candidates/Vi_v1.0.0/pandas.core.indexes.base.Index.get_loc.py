    @Appender(_index_shared_docs["get_loc"])
    def get_loc(self, key, method=None, tolerance=None):
        if method is None:
            if tolerance is not None:
                raise ValueError(
                    "tolerance argument only valid if using pad, "
                    "backfill or nearest lookups"
                )
            try:
                return self._engine.get_loc(key)
            except KeyError:
                return self._engine.get_loc(self._maybe_cast_indexer(key))
        indexer = self.get_indexer([key], method=method, tolerance=tolerance)
        if indexer.ndim > 1 or indexer.size > 1:
            raise TypeError("get_loc requires scalar valued input")
        loc = indexer.item()
        if loc == -1:
            raise KeyError(key)
        return loc
