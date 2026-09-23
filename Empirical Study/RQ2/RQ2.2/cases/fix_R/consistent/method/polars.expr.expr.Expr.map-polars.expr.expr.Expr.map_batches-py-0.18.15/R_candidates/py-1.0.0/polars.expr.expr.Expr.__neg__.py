    def __neg__(self) -> Expr:
        return self._from_pyexpr(-self._pyexpr)
