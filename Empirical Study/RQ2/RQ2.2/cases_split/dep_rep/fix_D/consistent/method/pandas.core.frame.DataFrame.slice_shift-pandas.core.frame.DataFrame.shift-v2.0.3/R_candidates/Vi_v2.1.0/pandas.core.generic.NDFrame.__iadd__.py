    @final
    def __iadd__(self, other) -> Self:
        # error: Unsupported left operand type for + ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__add__)  # type: ignore[operator]
