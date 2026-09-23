    @property
    def nbytes(self):
        return self._codes.nbytes + self._categories.values.nbytes
