    def __abs__(self) -> PandasArray:
        return type(self)(abs(self._ndarray))
