    @cache_readonly
    def dtype(self) -> FloatingDtype:
        return FLOAT_STR_TO_DTYPE[str(self._data.dtype)]
