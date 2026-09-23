    @cache_readonly
    def _reso(self) -> int:
        return get_unit_from_dtype(self._ndarray.dtype)
