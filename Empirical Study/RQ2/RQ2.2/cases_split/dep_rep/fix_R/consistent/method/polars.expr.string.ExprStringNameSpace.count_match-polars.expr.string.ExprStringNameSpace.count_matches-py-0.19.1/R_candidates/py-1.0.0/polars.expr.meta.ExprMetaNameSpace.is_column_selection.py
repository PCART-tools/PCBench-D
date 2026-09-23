    def is_column_selection(self, *, allow_aliasing: bool = False) -> bool:
        """
        Indicate if this expression only selects columns (optionally with aliasing).

        This can include bare columns, column matches by regex or dtype, selectors
        and exclude ops, and (optionally) column/expression aliasing.

        .. versionadded:: 0.20.30

        Parameters
        ----------
        allow_aliasing
            If False (default), any aliasing is not considered pure column selection.
            Set True to allow for column selection that also includes aliasing.

        Examples
        --------
        >>> import polars.selectors as cs
        >>> e = pl.col("foo")
        >>> e.meta.is_column_selection()
        True
        >>> e = pl.col("foo").alias("bar")
        >>> e.meta.is_column_selection()
        False
        >>> e.meta.is_column_selection(allow_aliasing=True)
        True
        >>> e = pl.col("foo") * pl.col("bar")
        >>> e.meta.is_column_selection()
        False
        >>> e = cs.starts_with("foo")
        >>> e.meta.is_column_selection()
        True
        >>> e = cs.starts_with("foo").exclude("foo!")
        >>> e.meta.is_column_selection()
        True
        """
        return self._pyexpr.meta_is_column_selection(allow_aliasing)
