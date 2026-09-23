    def count(self) -> Self:
        """
        Return the number of non-null elements in the column.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        See Also
        --------
        len

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [None, 4, 4]})
        >>> df.select(pl.all().count())
        shape: (1, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ u32 ┆ u32 │
        ╞═════╪═════╡
        │ 3   ┆ 2   │
        └─────┴─────┘
        """
        return self._from_pyexpr(self._pyexpr.count())
