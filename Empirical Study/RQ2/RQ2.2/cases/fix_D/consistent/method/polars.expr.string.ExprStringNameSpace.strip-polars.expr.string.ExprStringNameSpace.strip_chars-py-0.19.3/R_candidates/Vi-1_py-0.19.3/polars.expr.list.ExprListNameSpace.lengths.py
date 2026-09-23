    def lengths(self) -> Expr:
        """
        Get the length of the arrays as UInt32.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2], "bar": [["a", "b"], ["c"]]})
        >>> df.select(pl.col("bar").list.lengths())
        shape: (2, 1)
        ┌─────┐
        │ bar │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 2   │
        │ 1   │
        └─────┘

        """
        return wrap_expr(self._pyexpr.list_lengths())
