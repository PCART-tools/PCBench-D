    def _selector_and(self, other: Expr) -> Expr:
        """& selectors."""
        return wrap_expr(self._pyexpr._meta_selector_and(other._pyexpr))
