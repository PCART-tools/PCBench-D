    @property
    def nbytes(self):
        return self._codes.nbytes + self.dtype.categories.values.nbytes
