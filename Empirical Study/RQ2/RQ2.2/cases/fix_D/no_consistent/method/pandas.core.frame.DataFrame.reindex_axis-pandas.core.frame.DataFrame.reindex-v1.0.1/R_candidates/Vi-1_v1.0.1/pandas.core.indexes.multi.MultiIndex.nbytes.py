    @cache_readonly
    def nbytes(self) -> int:
        """ return the number of bytes in the underlying data """
        return self._nbytes(False)
