    @property
    def _pyexpr(self) -> PyExpr:
        return self._chained_then.otherwise(F.lit(None)._pyexpr)
