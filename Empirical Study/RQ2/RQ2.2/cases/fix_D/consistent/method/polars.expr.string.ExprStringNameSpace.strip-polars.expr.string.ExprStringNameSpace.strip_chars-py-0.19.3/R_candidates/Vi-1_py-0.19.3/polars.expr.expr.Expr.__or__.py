    def __or__(self, other: Expr | int | bool) -> Self:
        return self._from_pyexpr(self._pyexpr._or(self._to_pyexpr(other)))
