    def __neg__(self) -> Self:
        return type(self)(pc.negate_checked(self._pa_array))
