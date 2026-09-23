    @Appender(_index_shared_docs['dropna'])
    def dropna(self, how='any'):
        if how not in ('any', 'all'):
            raise ValueError("invalid how option: {0}".format(how))

        if self.hasnans:
            return self._shallow_copy(self.values[~self._isnan])
        return self._shallow_copy()
