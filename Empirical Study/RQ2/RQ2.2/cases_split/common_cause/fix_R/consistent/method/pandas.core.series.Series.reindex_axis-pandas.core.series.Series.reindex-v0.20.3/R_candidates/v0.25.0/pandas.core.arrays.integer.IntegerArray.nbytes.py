    @property
    def nbytes(self):
        return self._data.nbytes + self._mask.nbytes
