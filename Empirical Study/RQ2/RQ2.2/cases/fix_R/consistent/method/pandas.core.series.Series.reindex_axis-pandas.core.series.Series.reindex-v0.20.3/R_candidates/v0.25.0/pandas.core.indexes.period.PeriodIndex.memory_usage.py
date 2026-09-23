    def memory_usage(self, deep=False):
        result = super().memory_usage(deep=deep)
        if hasattr(self, "_cache") and "_int64index" in self._cache:
            result += self._int64index.memory_usage(deep=deep)
        return result
