    @Appender(ibase._index_shared_docs['copy'])
    def copy(self, name=None, deep=False, dtype=None, **kwargs):
        self._validate_dtype(dtype)
        if name is None:
            name = self.name
        return RangeIndex._simple_new(
            name=name, **dict(self._get_data_as_items()))
