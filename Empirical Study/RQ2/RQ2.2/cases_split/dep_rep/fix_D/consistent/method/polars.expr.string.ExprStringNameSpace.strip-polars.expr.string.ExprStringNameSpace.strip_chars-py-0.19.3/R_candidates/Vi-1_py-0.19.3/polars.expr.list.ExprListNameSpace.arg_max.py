    def arg_max(self) -> Expr:
        """
        Retrieve the index of the maximum value in every sublist.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 2], [2, 1]],
        ...     }
        ... )
        >>> df.select(pl.col("a").list.arg_max())
        shape: (2, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 1   │
        │ 0   │
        └─────┘

        """
        return wrap_expr(self._pyexpr.list_arg_max())
