    @property
    def memory_usage_bytes(self) -> int:
        """Memory usage in bytes.

        Returns
        -------
        memory_usage_bytes : int
            Object's total memory usage in bytes.
        """
        deep = self.memory_usage == "deep"
        return self.data.memory_usage(index=True, deep=deep)
