    def __neg__(self) -> NumpyExtensionArray:
        return type(self)(-self._ndarray)
