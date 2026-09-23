    def undo_aliases(self) -> Expr:
        """
        Undo any renaming operation like `alias` or `name.keep`.

        Examples
        --------
        >>> e = pl.col("foo").alias("bar")
        >>> e.meta.undo_aliases().meta == pl.col("foo")
        True
        >>> e = pl.col("foo").sum().over("bar")
        >>> e.name.keep().meta.undo_aliases().meta == e
        True

        """
        return wrap_expr(self._pyexpr.meta_undo_aliases())
