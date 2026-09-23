    @final
    def __ifloordiv__(self, other) -> Self:
        # error: Unsupported left operand type for // ("Type[NDFrame]")
        return self._inplace_method(
            other, type(self).__floordiv__  # type: ignore[operator]
        )
