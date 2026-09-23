    @final
    def __imul__(self, other) -> Self:
        # error: Unsupported left operand type for * ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__mul__)  # type: ignore[operator]
