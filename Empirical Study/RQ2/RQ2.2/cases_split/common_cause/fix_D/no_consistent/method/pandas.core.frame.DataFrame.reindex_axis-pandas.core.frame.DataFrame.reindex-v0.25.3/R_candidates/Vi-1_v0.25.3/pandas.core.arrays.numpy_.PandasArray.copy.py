    def copy(self):
        return type(self)(self._ndarray.copy())
