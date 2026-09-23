    @doc(IndexOpsMixin._memory_usage)
    def memory_usage(self, deep: bool = False) -> int:
        result = self._memory_usage(deep=deep)

        # include our engine hashtable
        result += self._engine.sizeof(deep=deep)
        return result
