    def __itruediv__(self: NDFrameT, other) -> NDFrameT:
        # error: Unsupported left operand type for / ("Type[NDFrame]")
        return self._inplace_method(
            other, type(self).__truediv__  # type: ignore[operator]
        )
