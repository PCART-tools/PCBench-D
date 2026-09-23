    def __abs__(self) -> Self:
        return type(self)(pc.abs_checked(self._pa_array))
