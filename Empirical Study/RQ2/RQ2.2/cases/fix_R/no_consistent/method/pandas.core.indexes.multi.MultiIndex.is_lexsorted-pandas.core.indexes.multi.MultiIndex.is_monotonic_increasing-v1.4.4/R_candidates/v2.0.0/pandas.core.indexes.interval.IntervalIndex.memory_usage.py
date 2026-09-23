    @Appender(Index.memory_usage.__doc__)  # type: ignore[has-type]
    def memory_usage(self, deep: bool = False) -> int:
        # we don't use an explicit engine
        # so return the bytes here
        return self.left.memory_usage(deep=deep) + self.right.memory_usage(deep=deep)
