    @doc(Index.memory_usage)
    def memory_usage(self, deep: bool = False) -> int:
        # we are overwriting our base class to avoid
        # computing .values here which could materialize
        # a tuple representation unnecessarily
        return self._nbytes(deep)
