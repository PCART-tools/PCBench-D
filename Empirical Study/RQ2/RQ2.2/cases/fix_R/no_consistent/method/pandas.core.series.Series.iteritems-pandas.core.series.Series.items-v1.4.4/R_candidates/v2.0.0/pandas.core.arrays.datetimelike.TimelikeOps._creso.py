    @cache_readonly
    def _creso(self) -> int:
        return get_unit_from_dtype(self._ndarray.dtype)
