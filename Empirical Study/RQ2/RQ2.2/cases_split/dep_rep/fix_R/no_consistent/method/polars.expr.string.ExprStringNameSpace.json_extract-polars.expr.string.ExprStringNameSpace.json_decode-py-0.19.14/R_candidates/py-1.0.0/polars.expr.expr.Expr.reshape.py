    def reshape(self, dimensions: tuple[int, ...]) -> Expr:
        """
        Reshape this Expr to a flat column or an Array column.

        Parameters
        ----------
        dimensions
            Tuple of the dimension sizes. If a -1 is used in any of the dimensions, that
            dimension is inferred.

        Returns
        -------
        Expr
            If a single dimension is given, results in an expression of the original
            data type.
            If a multiple dimensions are given, results in an expression of data type
            :class:`Array` with shape `dimensions`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        >>> square = df.select(pl.col("foo").reshape((3, 3)))
        >>> square
        shape: (3, 1)
        ┌───────────────┐
        │ foo           │
        │ ---           │
        │ array[i64, 3] │
        ╞═══════════════╡
        │ [1, 2, 3]     │
        │ [4, 5, 6]     │
        │ [7, 8, 9]     │
        └───────────────┘
        >>> square.select(pl.col("foo").reshape((9,)))
        shape: (9, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 1   │
        │ 2   │
        │ 3   │
        │ 4   │
        │ 5   │
        │ 6   │
        │ 7   │
        │ 8   │
        │ 9   │
        └─────┘

        See Also
        --------
        Expr.list.explode : Explode a list column.
        """
        return self._from_pyexpr(self._pyexpr.reshape(dimensions))
