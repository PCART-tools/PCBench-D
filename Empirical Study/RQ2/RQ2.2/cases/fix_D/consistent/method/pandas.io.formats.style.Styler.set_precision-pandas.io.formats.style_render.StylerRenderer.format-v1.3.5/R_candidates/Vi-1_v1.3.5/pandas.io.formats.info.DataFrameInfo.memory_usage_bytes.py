    @property
    def memory_usage_bytes(self) -> int:
        if self.memory_usage == "deep":
            deep = True
        else:
            deep = False
        return self.data.memory_usage(index=True, deep=deep).sum()
