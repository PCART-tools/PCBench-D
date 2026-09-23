    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        if level is not None:
            self._validate_index_level(level)
        return algorithms.isin(np.array(self), values)
