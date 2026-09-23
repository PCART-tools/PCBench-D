    @deprecate_renamed_function("set_intersection", version="0.18.10")
    def intersection(self, other: IntoExpr) -> Expr:
        """
        Compute the SET INTERSECTION between the elements in this list and the elements of ``other``.

        .. deprecated:: 0.18.10
            This method has been renamed to ``Expr.list.set_intersection``.

        """  # noqa: W505
        return self.set_intersection(other)
