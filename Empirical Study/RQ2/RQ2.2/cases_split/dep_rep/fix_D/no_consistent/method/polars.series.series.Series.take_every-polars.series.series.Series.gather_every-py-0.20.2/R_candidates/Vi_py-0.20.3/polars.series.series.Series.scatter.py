    def scatter(
        self,
        indices: Series | np.ndarray[Any, Any] | Sequence[int] | int,
        values: (
            int
            | float
            | str
            | bool
            | date
            | datetime
            | Sequence[int]
            | Sequence[float]
            | Sequence[bool]
            | Sequence[str]
            | Sequence[date]
            | Sequence[datetime]
            | Series
            | None
        ),
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

        >>> s.to_frame().with_row_count("row_nr").select(
        ...     pl.when(pl.col("row_nr") == 1).then(10).otherwise(pl.col("a"))
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
        if isinstance(indices, int):
            indices = [indices]
        if len(indices) == 0:
            return self

        indices = Series("", indices)
        if isinstance(values, (int, float, bool, str)) or (values is None):
            values = Series("", [values])

            # if we need to set more than a single value, we extend it
            if len(indices) > 0:
                values = values.extend_constant(values[0], len(indices) - 1)
        elif not isinstance(values, Series):
            values = Series("", values)
        self._s.scatter(indices._s, values._s)
        return self
