    @cache_readonly
    def dtype(self) -> _IntegerDtype:
        return INT_STR_TO_DTYPE[str(self._data.dtype)]
