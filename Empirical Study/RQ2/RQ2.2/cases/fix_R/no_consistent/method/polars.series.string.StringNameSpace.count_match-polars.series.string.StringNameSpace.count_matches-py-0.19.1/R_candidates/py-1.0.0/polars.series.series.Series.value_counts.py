    def value_counts(
        self,
        *,
        sort: bool = False,
        parallel: bool = False,
        name: str | None = None,
        normalize: bool = False,
    ) -> DataFrame:
        """
        Count the occurrences of unique values.

        Parameters
        ----------
        sort
            Sort the output by count in descending order.
            If set to `False` (default), the order of the output is random.
        parallel
            Execute the computation in parallel.

            .. note::
                This option should likely not be enabled in a group by context,
                as the computation is already parallelized per group.
        name
            Give the resulting count column a specific name;
            if `normalize` is True defaults to "count",
            otherwise defaults to "proportion".
        normalize
            If true gives relative frequencies of the unique values

        Returns
        -------
        DataFrame
            Mapping of unique values to their count.

        Examples
        --------
        >>> s = pl.Series("color", ["red", "blue", "red", "green", "blue", "blue"])
        >>> s.value_counts()  # doctest: +IGNORE_RESULT
        shape: (3, 2)
        ┌───────┬───────┐
        │ color ┆ count │
        │ ---   ┆ ---   │
        │ str   ┆ u32   │
        ╞═══════╪═══════╡
        │ red   ┆ 2     │
        │ green ┆ 1     │
        │ blue  ┆ 3     │
        └───────┴───────┘

        Sort the output by count and customize the count column name.

        >>> s.value_counts(sort=True, name="n")
        shape: (3, 2)
        ┌───────┬─────┐
        │ color ┆ n   │
        │ ---   ┆ --- │
        │ str   ┆ u32 │
        ╞═══════╪═════╡
        │ blue  ┆ 3   │
        │ red   ┆ 2   │
        │ green ┆ 1   │
        └───────┴─────┘
        """
        if name is None:
            if normalize:
                name = "proportion"
            else:
                name = "count"
        return pl.DataFrame._from_pydf(
            self._s.value_counts(
                sort=sort, parallel=parallel, name=name, normalize=normalize
            )
        )
