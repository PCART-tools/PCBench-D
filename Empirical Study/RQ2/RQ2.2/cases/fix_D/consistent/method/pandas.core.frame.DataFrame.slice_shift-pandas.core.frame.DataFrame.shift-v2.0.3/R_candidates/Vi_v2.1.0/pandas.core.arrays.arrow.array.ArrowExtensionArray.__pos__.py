    def __pos__(self) -> Self:
        return type(self)(self._pa_array)
