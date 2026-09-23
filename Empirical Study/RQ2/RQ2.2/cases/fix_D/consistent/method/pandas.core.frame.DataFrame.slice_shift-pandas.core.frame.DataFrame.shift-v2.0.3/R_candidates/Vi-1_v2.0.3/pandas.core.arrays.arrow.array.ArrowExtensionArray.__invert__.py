    def __invert__(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        return type(self)(pc.invert(self._data))
