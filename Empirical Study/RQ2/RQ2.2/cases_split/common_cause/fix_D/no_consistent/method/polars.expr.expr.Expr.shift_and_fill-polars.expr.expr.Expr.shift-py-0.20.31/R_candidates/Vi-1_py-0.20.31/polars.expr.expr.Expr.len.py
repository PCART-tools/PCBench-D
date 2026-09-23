    def len(self) -> Self:
        """
        Return the number of elements in the column.

        Null values count towards the total.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        See Also
        --------
        count

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [None, 4, 4]})
        >>> df.select(pl.all().len())
        shape: (1, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ u32 ┆ u32 │
        ╞═════╪═════╡
        │ 3   ┆ 3   │
        └─────┴─────┘
        """
        return self._from_pyexpr(self._pyexpr.len())
