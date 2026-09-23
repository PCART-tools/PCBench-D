    def __floordiv__(self, other: Any) -> Self:
        return self._from_pyexpr(self._pyexpr // self._to_pyexpr(other))
