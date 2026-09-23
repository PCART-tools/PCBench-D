    def __invert__(self) -> PandasArray:
        return type(self)(~self._ndarray)
