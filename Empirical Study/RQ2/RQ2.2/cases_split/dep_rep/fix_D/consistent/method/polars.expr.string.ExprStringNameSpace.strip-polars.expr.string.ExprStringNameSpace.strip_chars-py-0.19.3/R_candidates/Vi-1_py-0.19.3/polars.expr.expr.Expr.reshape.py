    def reshape(self, dimensions: tuple[int, ...]) -> Self:
        """
        Reshape this Expr to a flat Series or a Series of Lists.

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
            :class:`List` with shape (rows, cols).

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        >>> df.select(pl.col("foo").reshape((3, 3)))
        shape: (3, 1)
        ┌───────────┐
        │ foo       │
        │ ---       │
        │ list[i64] │
        ╞═══════════╡
        │ [1, 2, 3] │
        │ [4, 5, 6] │
        │ [7, 8, 9] │
        └───────────┘

        See Also
        --------
        Expr.list.explode : Explode a list column.

        """
        return self._from_pyexpr(self._pyexpr.reshape(dimensions))
