    def set_at_idx(
        self,
        idx: Series | np.ndarray[Any, Any] | Sequence[int] | int,
        value: (
            int
            | float
            | str
            | bool
            | Sequence[int]
            | Sequence[float]
            | Sequence[bool]
            | Sequence[str]
            | Sequence[date]
            | Sequence[datetime]
            | date
            | datetime
            | Series
            | None
        ),
    ) -> Series:
        """
        Set values at the index locations.

        Parameters
        ----------
        idx
            Integers representing the index locations.
        value
            replacement values.

        Returns
        -------
        Series
            The mutated series.

        Notes
        -----
        Use of this function is frequently an anti-pattern, as it can
        block optimisation (predicate pushdown, etc). Consider using
        `pl.when(predicate).then(value).otherwise(self)` instead.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.set_at_idx(1, 10)
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
        if isinstance(idx, int):
            idx = [idx]
        if len(idx) == 0:
            return self

        idx = Series("", idx)
        if isinstance(value, (int, float, bool, str)) or (value is None):
            value = Series("", [value])

            # if we need to set more than a single value, we extend it
            if len(idx) > 0:
                value = value.extend_constant(value[0], len(idx) - 1)
        elif not isinstance(value, Series):
            value = Series("", value)
        self._s.set_at_idx(idx._s, value._s)
        return self
