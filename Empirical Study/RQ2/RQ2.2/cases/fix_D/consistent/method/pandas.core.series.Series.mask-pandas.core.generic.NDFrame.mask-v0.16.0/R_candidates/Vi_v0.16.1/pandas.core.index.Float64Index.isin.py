    @Appender(Index.isin.__doc__)
    def isin(self, values, level=None):
        value_set = set(values)
        if level is not None:
            self._validate_index_level(level)
        return lib.ismember_nans(np.array(self), value_set,
                                 isnull(list(value_set)).any())
