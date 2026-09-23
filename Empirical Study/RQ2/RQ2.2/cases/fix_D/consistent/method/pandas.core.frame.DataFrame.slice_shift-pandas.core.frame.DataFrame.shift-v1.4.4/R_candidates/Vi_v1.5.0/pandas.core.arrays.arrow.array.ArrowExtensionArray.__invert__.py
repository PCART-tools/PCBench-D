    def __invert__(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        if pa_version_under2p0:
            raise NotImplementedError("__invert__ not implement for pyarrow < 2.0")
        return type(self)(pc.invert(self._data))
