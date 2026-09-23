    @Appender(IndexOpsMixin.memory_usage.__doc__)
    def memory_usage(self, deep=False):
        result = super(Index, self).memory_usage(deep=deep)

        # include our engine hashtable
        result += self._engine.sizeof(deep=deep)
        return result
