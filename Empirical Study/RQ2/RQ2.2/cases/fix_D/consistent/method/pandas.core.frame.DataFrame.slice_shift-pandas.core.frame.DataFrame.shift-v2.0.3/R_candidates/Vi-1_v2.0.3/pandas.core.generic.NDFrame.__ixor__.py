    def __ixor__(self: NDFrameT, other) -> NDFrameT:
        # error: Unsupported left operand type for ^ ("Type[NDFrame]")
        return self._inplace_method(other, type(self).__xor__)  # type: ignore[operator]
