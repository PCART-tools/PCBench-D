    @deprecate_renamed_function("is_first_distinct", version="0.19.3")
    def is_first(self) -> Self:
        """
        Return a boolean mask indicating the first occurrence of each distinct value.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`Expr.is_first_distinct`.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.
        """
        return self.is_first_distinct()
