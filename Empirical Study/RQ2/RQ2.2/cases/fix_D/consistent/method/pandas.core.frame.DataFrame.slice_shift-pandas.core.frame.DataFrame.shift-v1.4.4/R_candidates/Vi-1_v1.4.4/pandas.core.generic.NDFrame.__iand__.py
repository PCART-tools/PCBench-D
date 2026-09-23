    def __iand__(self, other):
        # error: Unsupported left operand type for & ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__and__)  # type: ignore[operator]
