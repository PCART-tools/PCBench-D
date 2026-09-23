    @cache_readonly
    def dtype(self) -> NumericDtype:
        mapping = self._dtype_cls._str_to_dtype_mapping()
        return mapping[str(self._data.dtype)]
