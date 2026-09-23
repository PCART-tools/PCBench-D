    def _selector_sub(self, other: Expr) -> Expr:
        """Subtract ('-') selectors."""
        return wrap_expr(self._pyexpr._meta_selector_sub(other._pyexpr))
