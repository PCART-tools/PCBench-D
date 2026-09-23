    @Appender(ibase._index_shared_docs["copy"])
    def copy(self, name=None, deep=False, dtype=None, **kwargs):
        self._validate_dtype(dtype)
        if name is None:
            name = self.name
        return self.from_range(self._range, name=name)
