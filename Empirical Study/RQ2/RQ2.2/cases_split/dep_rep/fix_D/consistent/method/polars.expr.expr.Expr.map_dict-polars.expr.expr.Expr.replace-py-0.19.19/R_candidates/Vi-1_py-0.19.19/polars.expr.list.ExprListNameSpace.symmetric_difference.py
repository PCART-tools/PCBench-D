    @deprecate_renamed_function("set_symmetric_difference", version="0.18.10")
    def symmetric_difference(self, other: IntoExpr) -> Expr:
        """
        Compute the SET SYMMETRIC DIFFERENCE between the elements in this list and the elements of `other`.

        .. deprecated:: 0.18.10
            This method has been renamed to `Expr.list.set_symmetric_difference`.

        """  # noqa: W505
        return self.set_symmetric_difference(other)
