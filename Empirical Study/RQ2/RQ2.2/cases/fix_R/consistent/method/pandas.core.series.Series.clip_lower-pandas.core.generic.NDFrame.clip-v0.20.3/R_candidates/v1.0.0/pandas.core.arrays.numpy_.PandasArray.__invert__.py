    def __invert__(self):
        return type(self)(~self._ndarray)
