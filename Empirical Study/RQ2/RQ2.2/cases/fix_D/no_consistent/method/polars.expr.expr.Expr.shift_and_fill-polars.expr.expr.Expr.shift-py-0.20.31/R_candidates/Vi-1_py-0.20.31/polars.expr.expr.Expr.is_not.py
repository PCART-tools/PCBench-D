    @deprecate_renamed_function("not_", version="0.19.2")
    def is_not(self) -> Self:
        """
        Negate a boolean expression.

        .. deprecated:: 0.19.2
            This method has been renamed to :func:`Expr.not_`.
        """
        return self.not_()
