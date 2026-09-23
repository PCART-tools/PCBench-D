    def _as_selector(self) -> Expr:
        """Turn this expression in a selector."""
        return wrap_expr(self._pyexpr._meta_as_selector())
