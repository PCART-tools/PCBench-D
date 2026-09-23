    def pop(self) -> list[Expr]:
        """
        Pop the latest expression and return the input(s) of the popped expression.

        Returns
        -------
        list of Expr
            A list of expressions which in most cases will have a unit length.
            This is not the case when an expression has multiple inputs.
            For instance in a ``fold`` expression.

        Examples
        --------
        >>> e = pl.col("foo").alias("bar")
        >>> first = e.meta.pop()[0]
        >>> first.meta == pl.col("foo")
        True
        >>> first.meta == pl.col("bar")
        False

        """
        return [wrap_expr(e) for e in self._pyexpr.meta_pop()]
