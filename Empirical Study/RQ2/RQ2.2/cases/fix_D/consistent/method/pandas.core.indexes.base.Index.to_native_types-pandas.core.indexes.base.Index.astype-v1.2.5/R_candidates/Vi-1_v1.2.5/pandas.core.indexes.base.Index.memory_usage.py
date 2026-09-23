    @doc(IndexOpsMixin.memory_usage)
    def memory_usage(self, deep: bool = False) -> int:
        result = super().memory_usage(deep=deep)

        # include our engine hashtable
        result += self._engine.sizeof(deep=deep)
        return result
