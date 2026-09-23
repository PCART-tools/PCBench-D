    @unstable()
    def cut(
        self,
        breaks: Sequence[float],
        *,
        labels: Sequence[str] | None = None,
        left_closed: bool = False,
        include_breaks: bool = False,
    ) -> Series:
        """
        Bin continuous values into discrete categories.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        breaks
            List of unique cut points.
        labels
            Names of the categories. The number of labels must be equal to the number
            of cut points plus one.
        left_closed
            Set the intervals to be left-closed instead of right-closed.
        include_breaks
            Include a column with the right endpoint of the bin each observation falls
            in. This will change the data type of the output from a
            :class:`Categorical` to a :class:`Struct`.

        Returns
        -------
        Series
            Series of data type :class:`Categorical` if `include_breaks` is set to
            `False` (default), otherwise a Series of data type :class:`Struct`.

        See Also
        --------
        qcut

        Examples
        --------
        Divide the column into three categories.

        >>> s = pl.Series("foo", [-2, -1, 0, 1, 2])
        >>> s.cut([-1, 1], labels=["a", "b", "c"])
        shape: (5,)
        Series: 'foo' [cat]
        [
                "a"
                "a"
                "b"
                "b"
                "c"
        ]

        Create a DataFrame with the breakpoint and category for each value.

        >>> cut = s.cut([-1, 1], include_breaks=True).alias("cut")
        >>> s.to_frame().with_columns(cut).unnest("cut")
        shape: (5, 3)
        ┌─────┬────────────┬────────────┐
        │ foo ┆ breakpoint ┆ category   │
        │ --- ┆ ---        ┆ ---        │
        │ i64 ┆ f64        ┆ cat        │
        ╞═════╪════════════╪════════════╡
        │ -2  ┆ -1.0       ┆ (-inf, -1] │
        │ -1  ┆ -1.0       ┆ (-inf, -1] │
        │ 0   ┆ 1.0        ┆ (-1, 1]    │
        │ 1   ┆ 1.0        ┆ (-1, 1]    │
        │ 2   ┆ inf        ┆ (1, inf]   │
        └─────┴────────────┴────────────┘
        """
