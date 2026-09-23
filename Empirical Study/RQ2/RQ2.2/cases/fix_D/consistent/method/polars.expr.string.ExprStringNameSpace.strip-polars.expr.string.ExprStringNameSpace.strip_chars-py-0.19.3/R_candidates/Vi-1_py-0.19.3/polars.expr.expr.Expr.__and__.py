    def __and__(self, other: Expr | int | bool) -> Self:
        return self._from_pyexpr(self._pyexpr._and(self._to_pyexpr(other)))
