    def slice(self, offset: int, length: int | None = None) -> Expr:
        """
        Create subslices of the string values of a String Series.

        Parameters
        ----------
        offset
            Start index. Negative indexing is supported.
        length
            Length of the slice. If set to `None` (default), the slice is taken to the
            end of the string.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["pear", None, "papaya", "dragonfruit"]})
        >>> df.with_columns(
        ...     pl.col("s").str.slice(-3).alias("s_sliced"),
        ... )
        shape: (4, 2)
        ┌─────────────┬──────────┐
        │ s           ┆ s_sliced │
        │ ---         ┆ ---      │
        │ str         ┆ str      │
        ╞═════════════╪══════════╡
        │ pear        ┆ ear      │
        │ null        ┆ null     │
        │ papaya      ┆ aya      │
        │ dragonfruit ┆ uit      │
        └─────────────┴──────────┘

        Using the optional `length` parameter

        >>> df.with_columns(
        ...     pl.col("s").str.slice(4, length=3).alias("s_sliced"),
        ... )
        shape: (4, 2)
        ┌─────────────┬──────────┐
        │ s           ┆ s_sliced │
        │ ---         ┆ ---      │
        │ str         ┆ str      │
        ╞═════════════╪══════════╡
        │ pear        ┆          │
        │ null        ┆ null     │
        │ papaya      ┆ ya       │
        │ dragonfruit ┆ onf      │
        └─────────────┴──────────┘

        """
        return wrap_expr(self._pyexpr.str_slice(offset, length))
