    @Appender(_index_shared_docs["dropna"])
    def dropna(self, how="any"):
        if how not in ("any", "all"):
            raise ValueError(f"invalid how option: {how}")

        if self.hasnans:
            return self._shallow_copy(self._values[~self._isnan])
        return self._shallow_copy()
