    @Appender(Index.dropna.__doc__)
    def dropna(self, how="any"):
        if how not in ("any", "all"):
            raise ValueError(f"invalid how option: {how}")

        if self.hasnans:
            return self._shallow_copy(self._data[~self._isnan])
        return self._shallow_copy()
