    def __imod__(self: NDFrameT, other) -> NDFrameT:
        # error: Unsupported left operand type for % ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__mod__)  # type: ignore[operator]
