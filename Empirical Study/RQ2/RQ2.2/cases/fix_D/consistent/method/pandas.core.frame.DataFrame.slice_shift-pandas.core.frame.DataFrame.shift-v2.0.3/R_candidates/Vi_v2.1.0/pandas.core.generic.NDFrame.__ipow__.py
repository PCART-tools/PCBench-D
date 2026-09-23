    @final
    def __ipow__(self, other) -> Self:
        # error: Unsupported left operand type for ** ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__pow__)  # type: ignore[operator]
