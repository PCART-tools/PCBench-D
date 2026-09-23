    def scatter(
        self,
        indices: Series | Iterable[int] | int | np.ndarray[Any, Any],
        values: Series | Iterable[PythonLiteral] | PythonLiteral | None,
    ) -> Series:
        """
        Set values at the index locations.

        Parameters
        ----------
        indices
            Integers representing the index locations.
        values
            Replacement values.

        Notes
        -----
        Use of this function is frequently an anti-pattern, as it can
        block optimization (predicate pushdown, etc). Consider using
        `pl.when(predicate).then(value).otherwise(self)` instead.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.scatter(1, 10)
        shape: (3,)
        Series: 'a' [i64]
        [
                1
                10
                3
        ]

        It is better to implement this as follows:

        >>> s.to_frame().with_row_index().select(
        ...     pl.when(pl.col("index") == 1).then(10).otherwise(pl.col("a"))
        ... )
        shape: (3, 1)
        ┌─────────┐
        │ literal │
        │ ---     │
        │ i64     │
        ╞═════════╡
        │ 1       │
        │ 10      │
        │ 3       │
        └─────────┘
        """
        if not isinstance(indices, Iterable):
            indices = [indices]  # type: ignore[list-item]
        indices = Series(values=indices)
        if indices.is_empty():
            return self

        if not isinstance(values, Series):
            if not isinstance(values, Iterable) or isinstance(values, str):
                values = [values]
            values = Series(values=values)

        self._s.scatter(indices._s, values._s)
        return self
