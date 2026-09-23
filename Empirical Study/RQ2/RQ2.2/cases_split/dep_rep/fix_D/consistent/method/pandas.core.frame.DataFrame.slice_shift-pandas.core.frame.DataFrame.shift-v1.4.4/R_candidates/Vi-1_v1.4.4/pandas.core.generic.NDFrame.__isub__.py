    def __isub__(self, other):
        # error: Unsupported left operand type for - ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__sub__)  # type: ignore[operator]
