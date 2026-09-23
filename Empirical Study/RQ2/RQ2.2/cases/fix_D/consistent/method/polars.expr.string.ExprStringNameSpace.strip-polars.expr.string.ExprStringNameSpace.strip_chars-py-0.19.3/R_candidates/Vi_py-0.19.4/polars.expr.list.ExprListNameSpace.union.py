    @deprecate_renamed_function("set_union", version="0.18.10")
    def union(self, other: IntoExpr) -> Expr:
        """
        Compute the SET UNION between the elements in this list and the elements of ``other``.

        .. deprecated:: 0.18.10
            This method has been renamed to ``Expr.list.set_union``.

        """  # noqa: W505
        return self.set_union(other)
