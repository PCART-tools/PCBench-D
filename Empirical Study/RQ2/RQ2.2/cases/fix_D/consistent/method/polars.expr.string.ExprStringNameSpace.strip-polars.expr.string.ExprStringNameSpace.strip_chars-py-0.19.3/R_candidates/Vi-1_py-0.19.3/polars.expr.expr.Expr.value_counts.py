    @deprecate_renamed_parameter("multithreaded", "parallel", version="0.19.0")
    def value_counts(self, *, sort: bool = False, parallel: bool = False) -> Self:
        """
        Count the occurrences of unique values.

        Parameters
        ----------
        sort
            Sort the output by count in descending order.
            If set to ``False`` (default), the order of the output is random.
        parallel
            Execute the computation in parallel.

            .. note::
                This option should likely not be enabled in a group by context,
                as the computation is already parallelized per group.

        Returns
        -------
        Expr
            Expression of data type :class:`Struct` with mapping of unique values to
            their count.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"color": ["red", "blue", "red", "green", "blue", "blue"]}
        ... )
        >>> df.select(pl.col("color").value_counts())  # doctest: +IGNORE_RESULT
        shape: (3, 1)
        ┌─────────────┐
        │ color       │
        │ ---         │
        │ struct[2]   │
        ╞═════════════╡
        │ {"red",2}   │
        │ {"green",1} │
        │ {"blue",3}  │
        └─────────────┘

        Sort the output by count.

        >>> df.select(pl.col("color").value_counts(sort=True))
        shape: (3, 1)
        ┌─────────────┐
        │ color       │
        │ ---         │
        │ struct[2]   │
        ╞═════════════╡
        │ {"blue",3}  │
        │ {"red",2}   │
        │ {"green",1} │
        └─────────────┘

        """
        return self._from_pyexpr(self._pyexpr.value_counts(sort, parallel))
