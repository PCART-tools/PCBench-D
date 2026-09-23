    def __le__(self, other: Any) -> Self:
        return self._from_pyexpr(self._pyexpr.lt_eq(self._to_expr(other)._pyexpr))
