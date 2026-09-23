    def __imod__(self, other):
        # error: Unsupported left operand type for % ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__mod__)  # type: ignore[operator]
