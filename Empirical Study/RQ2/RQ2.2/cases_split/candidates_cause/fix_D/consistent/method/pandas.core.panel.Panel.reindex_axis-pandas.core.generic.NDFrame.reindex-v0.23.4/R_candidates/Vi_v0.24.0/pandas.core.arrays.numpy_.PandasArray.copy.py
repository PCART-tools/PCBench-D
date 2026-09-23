    def copy(self, deep=False):
        return type(self)(self._ndarray.copy())
