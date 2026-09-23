    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        value_set = set(values)
        if level is not None:
            self._validate_index_level(level)
        return lib.ismember_nans(self._array_values(), value_set,
                                 isnull(list(value_set)).any())
