    @final
    def __itruediv__(self, other) -> Self:
        # error: Unsupported left operand type for / ("Type[NDFrame]")
        return self._inplace_method(
            other, type(self).__truediv__  # type: ignore[operator]
        )
