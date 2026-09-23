    def _to_pyexpr(self, other: Any) -> PyExpr:
        return self._to_expr(other)._pyexpr
