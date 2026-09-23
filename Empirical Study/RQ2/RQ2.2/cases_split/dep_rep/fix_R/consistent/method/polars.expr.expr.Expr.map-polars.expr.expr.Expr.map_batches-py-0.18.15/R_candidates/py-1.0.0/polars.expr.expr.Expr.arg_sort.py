    def arg_sort(self, *, descending: bool = False, nulls_last: bool = False) -> Expr:
        """
        Get the index values that would sort this column.

        Parameters
        ----------
        descending
            Sort in descending (descending) order.
        nulls_last
            Place null values last instead of first.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        See Also
        --------
        Expr.gather: Take values by index.
        Expr.rank : Get the rank of each row.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [20, 10, 30],
        ...         "b": [1, 2, 3],
        ...     }
        ... )
        >>> df.select(pl.col("a").arg_sort())
        shape: (3, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 1   │
        │ 0   │
        │ 2   │
        └─────┘

        Use gather to apply the arg sort to other columns.

        >>> df.select(pl.col("b").gather(pl.col("a").arg_sort()))
        shape: (3, 1)
        ┌─────┐
        │ b   │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 2   │
        │ 1   │
        │ 3   │
        └─────┘
        """
        return self._from_pyexpr(self._pyexpr.arg_sort(descending, nulls_last))
