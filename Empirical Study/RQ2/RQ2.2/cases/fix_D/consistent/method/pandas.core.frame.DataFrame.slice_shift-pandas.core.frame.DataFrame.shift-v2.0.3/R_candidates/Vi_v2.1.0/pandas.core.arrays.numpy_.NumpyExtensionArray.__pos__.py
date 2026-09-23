    def __pos__(self) -> NumpyExtensionArray:
        return type(self)(+self._ndarray)
