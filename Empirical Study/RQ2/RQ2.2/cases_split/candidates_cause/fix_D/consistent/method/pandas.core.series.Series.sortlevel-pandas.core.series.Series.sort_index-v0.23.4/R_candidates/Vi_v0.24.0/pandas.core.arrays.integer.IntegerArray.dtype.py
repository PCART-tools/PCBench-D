    @cache_readonly
    def dtype(self):
        return _dtypes[str(self._data.dtype)]
