    @property
    def memory_usage_bytes(self) -> int:
        deep = self.memory_usage == "deep"
        return self.data.memory_usage(index=True, deep=deep).sum()
