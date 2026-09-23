    def __abs__(self) -> NumpyExtensionArray:
        return type(self)(abs(self._ndarray))
