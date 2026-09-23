    def _selector_xor(self, other: Expr) -> Expr:
        """Xor ('^') selectors."""
        return wrap_expr(self._pyexpr._meta_selector_xor(other._pyexpr))
