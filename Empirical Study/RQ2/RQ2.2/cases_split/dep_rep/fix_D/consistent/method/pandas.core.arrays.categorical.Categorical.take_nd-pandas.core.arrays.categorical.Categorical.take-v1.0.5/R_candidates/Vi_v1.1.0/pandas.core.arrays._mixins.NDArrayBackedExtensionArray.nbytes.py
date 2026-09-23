    @cache_readonly
    def nbytes(self) -> int:
        return self._ndarray.nbytes
