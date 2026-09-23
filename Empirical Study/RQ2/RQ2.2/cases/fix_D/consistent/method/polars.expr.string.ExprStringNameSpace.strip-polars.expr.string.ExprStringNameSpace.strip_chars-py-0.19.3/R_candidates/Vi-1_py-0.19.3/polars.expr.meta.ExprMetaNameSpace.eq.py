    def eq(self, other: ExprMetaNameSpace | Expr) -> bool:
        """
        Indicate if this expression is the same as another expression.

        Examples
        --------
        >>> foo_bar = pl.col("foo").alias("bar")
        >>> foo = pl.col("foo")
        >>> foo_bar.meta.eq(foo)
        False
        >>> foo_bar2 = pl.col("foo").alias("bar")
        >>> foo_bar.meta.eq(foo_bar2)
        True

        """
        return self._pyexpr.meta_eq(other._pyexpr)
