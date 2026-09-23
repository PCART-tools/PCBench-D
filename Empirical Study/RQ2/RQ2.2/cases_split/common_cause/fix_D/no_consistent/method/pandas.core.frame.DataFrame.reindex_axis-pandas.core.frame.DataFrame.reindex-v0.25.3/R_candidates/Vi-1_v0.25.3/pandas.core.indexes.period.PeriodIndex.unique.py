    @Appender(Index.unique.__doc__)
    def unique(self, level=None):
        # override the Index.unique method for performance GH#23083
        if level is not None:
            # this should never occur, but is retained to make the signature
            # match Index.unique
            self._validate_index_level(level)

        values = self._ndarray_values
        result = unique1d(values)
        return self._shallow_copy(result)
