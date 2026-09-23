    @property
    def nbytes(self) -> int:
        return self._data.nbytes + self._mask.nbytes
