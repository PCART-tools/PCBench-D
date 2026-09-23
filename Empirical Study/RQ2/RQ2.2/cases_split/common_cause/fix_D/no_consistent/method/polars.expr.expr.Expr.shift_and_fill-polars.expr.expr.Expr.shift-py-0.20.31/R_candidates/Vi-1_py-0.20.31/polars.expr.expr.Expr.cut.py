    @unstable()
    def cut(
        self,
        breaks: Sequence[float],
        *,
        labels: Sequence[str] | None = None,
        left_closed: bool = False,
        include_breaks: bool = False,
    ) -> Self:
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
        Expr
            Expression of data type :class:`Categorical` if `include_breaks` is set to
            `False` (default), otherwise an expression of data type :class:`Struct`.

        See Also
        --------
        qcut

        Examples
        --------
        Divide a column into three categories.

        >>> df = pl.DataFrame({"foo": [-2, -1, 0, 1, 2]})
        >>> df.with_columns(
        ...     pl.col("foo").cut([-1, 1], labels=["a", "b", "c"]).alias("cut")
        ... )
        shape: (5, 2)
        ┌─────┬─────┐
        │ foo ┆ cut │
        │ --- ┆ --- │
        │ i64 ┆ cat │
        ╞═════╪═════╡
        │ -2  ┆ a   │
        │ -1  ┆ a   │
        │ 0   ┆ b   │
        │ 1   ┆ b   │
        │ 2   ┆ c   │
        └─────┴─────┘

        Add both the category and the breakpoint.

        >>> df.with_columns(
        ...     pl.col("foo").cut([-1, 1], include_breaks=True).alias("cut")
        ... ).unnest("cut")
        shape: (5, 3)
        ┌─────┬──────┬────────────┐
        │ foo ┆ brk  ┆ foo_bin    │
        │ --- ┆ ---  ┆ ---        │
        │ i64 ┆ f64  ┆ cat        │
        ╞═════╪══════╪════════════╡
        │ -2  ┆ -1.0 ┆ (-inf, -1] │
        │ -1  ┆ -1.0 ┆ (-inf, -1] │
        │ 0   ┆ 1.0  ┆ (-1, 1]    │
        │ 1   ┆ 1.0  ┆ (-1, 1]    │
        │ 2   ┆ inf  ┆ (1, inf]   │
        └─────┴──────┴────────────┘
        """
        return self._from_pyexpr(
            self._pyexpr.cut(breaks, labels, left_closed, include_breaks)
        )
