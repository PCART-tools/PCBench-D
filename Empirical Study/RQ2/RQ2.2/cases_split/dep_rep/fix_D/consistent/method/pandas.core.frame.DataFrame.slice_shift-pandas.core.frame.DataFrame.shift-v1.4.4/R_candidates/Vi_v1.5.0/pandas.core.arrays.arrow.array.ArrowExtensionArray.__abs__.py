    def __abs__(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        return type(self)(pc.abs_checked(self._data))
