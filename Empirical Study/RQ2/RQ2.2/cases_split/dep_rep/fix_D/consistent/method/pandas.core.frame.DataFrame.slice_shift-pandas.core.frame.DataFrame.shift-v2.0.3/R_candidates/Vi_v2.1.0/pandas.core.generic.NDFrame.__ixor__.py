    @final
    def __ixor__(self, other) -> Self:
        # error: Unsupported left operand type for ^ ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__xor__)  # type: ignore[operator]
