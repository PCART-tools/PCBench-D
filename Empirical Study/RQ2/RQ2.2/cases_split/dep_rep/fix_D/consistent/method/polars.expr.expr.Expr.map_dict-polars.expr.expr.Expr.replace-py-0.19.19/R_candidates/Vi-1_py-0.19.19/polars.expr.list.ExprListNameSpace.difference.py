    @deprecate_renamed_function("set_difference", version="0.18.10")
    def difference(self, other: IntoExpr) -> Expr:
        """
        Compute the SET DIFFERENCE between the elements in this list and the elements of `other`.

        .. deprecated:: 0.18.10
            This method has been renamed to `Expr.list.set_difference`.

        """  # noqa: W505
        return self.set_difference(other)
