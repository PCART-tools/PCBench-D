    def __iadd__(self: NDFrameT, other) -> NDFrameT:
        # error: Unsupported left operand type for + ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__add__)  # type: ignore[operator]
