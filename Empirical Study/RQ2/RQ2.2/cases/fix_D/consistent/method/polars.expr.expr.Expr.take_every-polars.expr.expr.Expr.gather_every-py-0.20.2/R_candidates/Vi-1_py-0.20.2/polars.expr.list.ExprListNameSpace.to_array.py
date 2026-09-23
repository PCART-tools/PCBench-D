    def to_array(self, width: int) -> Expr:
        """
        Convert a List column into an Array column with the same inner data type.

        Parameters
        ----------
        width
            Width of the resulting Array column.

        Returns
        -------
        Expr
            Expression of data type :class:`Array`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={"a": [[1, 2], [3, 4]]},
        ...     schema={"a": pl.List(pl.Int8)},
        ... )
        >>> df.with_columns(array=pl.col("a").list.to_array(2))
        shape: (2, 2)
        ┌──────────┬──────────────┐
        │ a        ┆ array        │
        │ ---      ┆ ---          │
        │ list[i8] ┆ array[i8, 2] │
        ╞══════════╪══════════════╡
        │ [1, 2]   ┆ [1, 2]       │
        │ [3, 4]   ┆ [3, 4]       │
        └──────────┴──────────────┘

        """
        return wrap_expr(self._pyexpr.list_to_array(width))
