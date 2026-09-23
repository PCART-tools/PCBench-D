    def __rand__(self, other: Any) -> Self:
        return self._from_pyexpr(self._to_pyexpr(other)._and(self._pyexpr))
