    def __pos__(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        return type(self)(self._data)
