    def ne(self, other: ExprMetaNameSpace | Expr) -> bool:
        """
        Indicate if this expression is NOT the same as another expression.

        Examples
        --------
        >>> foo_bar = pl.col("foo").alias("bar")
        >>> foo = pl.col("foo")
        >>> foo_bar.meta.ne(foo)
        True
        >>> foo_bar2 = pl.col("foo").alias("bar")
        >>> foo_bar.meta.ne(foo_bar2)
        False

        """
        return not self.eq(other)
