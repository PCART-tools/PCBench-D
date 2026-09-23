    def __neg__(self) -> PandasArray:
        return type(self)(-self._ndarray)
