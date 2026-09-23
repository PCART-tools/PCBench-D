    @property
    def memory_usage_bytes(self) -> int:
        """Memory usage in bytes.

        Returns
        -------
        memory_usage_bytes : int
            Object's total memory usage in bytes.
        """
        if self.memory_usage == "deep":
            deep = True
        else:
            deep = False
        return self.data.memory_usage(index=True, deep=deep)
