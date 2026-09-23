    @property
    def _pyexpr(self) -> PyExpr:
        return self._then.otherwise(F.lit(None)._pyexpr)
