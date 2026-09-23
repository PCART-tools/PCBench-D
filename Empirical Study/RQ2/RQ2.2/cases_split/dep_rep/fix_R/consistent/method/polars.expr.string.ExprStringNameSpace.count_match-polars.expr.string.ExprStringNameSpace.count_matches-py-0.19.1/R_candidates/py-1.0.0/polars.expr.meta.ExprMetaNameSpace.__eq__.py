    def __eq__(self, other: ExprMetaNameSpace | Expr) -> bool:  # type: ignore[override]
        return self._pyexpr.meta_eq(other._pyexpr)
