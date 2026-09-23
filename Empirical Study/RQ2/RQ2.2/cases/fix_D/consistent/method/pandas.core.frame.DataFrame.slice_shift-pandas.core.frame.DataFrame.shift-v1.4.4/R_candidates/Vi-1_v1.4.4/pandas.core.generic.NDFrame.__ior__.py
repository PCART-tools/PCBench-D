    def __ior__(self, other):
        # error: Unsupported left operand type for | ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__or__)  # type: ignore[operator]
