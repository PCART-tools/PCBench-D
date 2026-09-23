    @cache_readonly
    def dtype(self) -> _IntegerDtype:
        return _dtypes[str(self._data.dtype)]
