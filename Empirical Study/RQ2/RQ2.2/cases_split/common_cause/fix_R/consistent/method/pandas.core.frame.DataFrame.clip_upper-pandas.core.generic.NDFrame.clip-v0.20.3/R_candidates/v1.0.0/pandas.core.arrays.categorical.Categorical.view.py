    def view(self, dtype=None):
        if dtype is not None:
            raise NotImplementedError(dtype)
        return self._constructor(values=self._codes, dtype=self.dtype, fastpath=True)
