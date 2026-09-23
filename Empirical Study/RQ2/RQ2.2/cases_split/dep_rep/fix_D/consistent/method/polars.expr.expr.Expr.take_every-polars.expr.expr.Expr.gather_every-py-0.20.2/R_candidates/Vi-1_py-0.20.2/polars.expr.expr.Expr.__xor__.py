    def __xor__(self, other: Expr | int | bool) -> Self:
        return self._from_pyexpr(self._pyexpr._xor(self._to_pyexpr(other)))
