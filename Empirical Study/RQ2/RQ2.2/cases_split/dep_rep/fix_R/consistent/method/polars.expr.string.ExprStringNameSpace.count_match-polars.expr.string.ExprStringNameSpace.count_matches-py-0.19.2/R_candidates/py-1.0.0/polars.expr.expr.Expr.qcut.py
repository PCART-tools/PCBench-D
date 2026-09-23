    @unstable()
    def qcut(
        self,
        quantiles: Sequence[float] | int,
        *,
        labels: Sequence[str] | None = None,
        left_closed: bool = False,
        allow_duplicates: bool = False,
        include_breaks: bool = False,
    ) -> Expr:
        """
        Bin continuous values into discrete categories based on their quantiles.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        quantiles
            Either a list of quantile probabilities between 0 and 1 or a positive
            integer determining the number of bins with uniform probability.
        labels
            Names of the categories. The number of labels must be equal to the number
            of categories.
        left_closed
            Set the intervals to be left-closed instead of right-closed.
        allow_duplicates
            If set to `True`, duplicates in the resulting quantiles are dropped,
            rather than raising a `DuplicateError`. This can happen even with unique
            probabilities, depending on the data.
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
        cut

        Examples
        --------
        Divide a column into three categories according to pre-defined quantile
        probabilities.

        >>> df = pl.DataFrame({"foo": [-2, -1, 0, 1, 2]})
        >>> df.with_columns(
        ...     pl.col("foo").qcut([0.25, 0.75], labels=["a", "b", "c"]).alias("qcut")
        ... )
        shape: (5, 2)
        ┌─────┬──────┐
        │ foo ┆ qcut │
        │ --- ┆ ---  │
        │ i64 ┆ cat  │
        ╞═════╪══════╡
        │ -2  ┆ a    │
        │ -1  ┆ a    │
        │ 0   ┆ b    │
        │ 1   ┆ b    │
        │ 2   ┆ c    │
        └─────┴──────┘

        Divide a column into two categories using uniform quantile probabilities.

        >>> df.with_columns(
        ...     pl.col("foo")
        ...     .qcut(2, labels=["low", "high"], left_closed=True)
        ...     .alias("qcut")
        ... )
        shape: (5, 2)
        ┌─────┬──────┐
        │ foo ┆ qcut │
        │ --- ┆ ---  │
        │ i64 ┆ cat  │
        ╞═════╪══════╡
        │ -2  ┆ low  │
        │ -1  ┆ low  │
        │ 0   ┆ high │
        │ 1   ┆ high │
        │ 2   ┆ high │
        └─────┴──────┘

        Add both the category and the breakpoint.

        >>> df.with_columns(
        ...     pl.col("foo").qcut([0.25, 0.75], include_breaks=True).alias("qcut")
        ... ).unnest("qcut")
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
        if isinstance(quantiles, int):
            pyexpr = self._pyexpr.qcut_uniform(
                quantiles, labels, left_closed, allow_duplicates, include_breaks
            )
        else:
            pyexpr = self._pyexpr.qcut(
                quantiles, labels, left_closed, allow_duplicates, include_breaks
            )

        return self._from_pyexpr(pyexpr)
