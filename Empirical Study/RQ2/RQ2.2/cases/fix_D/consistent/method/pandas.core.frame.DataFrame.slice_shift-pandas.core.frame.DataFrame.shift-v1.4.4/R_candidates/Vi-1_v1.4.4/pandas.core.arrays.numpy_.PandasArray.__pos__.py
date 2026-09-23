    def __pos__(self) -> PandasArray:
        return type(self)(+self._ndarray)
