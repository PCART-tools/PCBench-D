    @deprecate_renamed_function("count_matches", version="0.19.3")
    def count_match(self, element: IntoExpr) -> Expr:
        """
        Count how often the value produced by `element` occurs.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`count_matches`.

        Parameters
        ----------
        element
            An expression that produces a single value

        """
        return self.count_matches(element)
