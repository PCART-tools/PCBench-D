    def _selector_add(self, other: Expr) -> Expr:
        """Add ('+') selectors."""
        return wrap_expr(self._pyexpr._meta_selector_add(other._pyexpr))
