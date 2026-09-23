    def __neg__(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        return type(self)(pc.negate_checked(self._data))
