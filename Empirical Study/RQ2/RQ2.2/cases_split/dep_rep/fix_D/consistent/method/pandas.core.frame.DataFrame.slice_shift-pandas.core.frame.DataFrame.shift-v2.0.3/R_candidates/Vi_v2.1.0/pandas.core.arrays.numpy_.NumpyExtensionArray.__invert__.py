    def __invert__(self) -> NumpyExtensionArray:
        return type(self)(~self._ndarray)
