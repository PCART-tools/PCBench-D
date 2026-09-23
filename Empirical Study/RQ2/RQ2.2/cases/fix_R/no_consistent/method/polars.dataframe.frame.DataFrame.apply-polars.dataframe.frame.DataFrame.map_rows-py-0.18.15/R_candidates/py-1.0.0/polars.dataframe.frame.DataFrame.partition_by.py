    def partition_by(
        self,
        by: ColumnNameOrSelector | Sequence[ColumnNameOrSelector],
        *more_by: ColumnNameOrSelector,
        maintain_order: bool = True,
        include_key: bool = True,
        as_dict: bool = False,
    ) -> list[DataFrame] | dict[tuple[object, ...], DataFrame]:
        """
        Group by the given columns and return the groups as separate dataframes.

        Parameters
        ----------
        by
            Column name(s) or selector(s) to group by.
        *more_by
            Additional names of columns to group by, specified as positional arguments.
        maintain_order
            Ensure that the order of the groups is consistent with the input data.
            This is slower than a default partition by operation.
        include_key
            Include the columns used to partition the DataFrame in the output.
        as_dict
            Return a dictionary instead of a list. The dictionary keys are tuples of
            the distinct group values that identify each group. If a single string
            was passed to `by`, the keys are a single value instead of a tuple.

        Examples
        --------
        Pass a single column name to partition by that column.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "c"],
        ...         "b": [1, 2, 1, 3, 3],
        ...         "c": [5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> df.partition_by("a")  # doctest: +IGNORE_RESULT
        [shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 5   │
        │ a   ┆ 1   ┆ 3   │
        └─────┴─────┴─────┘,
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ b   ┆ 2   ┆ 4   │
        │ b   ┆ 3   ┆ 2   │
        └─────┴─────┴─────┘,
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ c   ┆ 3   ┆ 1   │
        └─────┴─────┴─────┘]

        Partition by multiple columns by either passing a list of column names, or by
        specifying each column name as a positional argument.

        >>> df.partition_by("a", "b")  # doctest: +IGNORE_RESULT
        [shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 5   │
        │ a   ┆ 1   ┆ 3   │
        └─────┴─────┴─────┘,
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ b   ┆ 2   ┆ 4   │
        └─────┴─────┴─────┘,
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ b   ┆ 3   ┆ 2   │
        └─────┴─────┴─────┘,
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ c   ┆ 3   ┆ 1   │
        └─────┴─────┴─────┘]

        Return the partitions as a dictionary by specifying `as_dict=True`.

        >>> import polars.selectors as cs
        >>> df.partition_by(cs.string(), as_dict=True)  # doctest: +IGNORE_RESULT
        {('a',): shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 5   │
        │ a   ┆ 1   ┆ 3   │
        └─────┴─────┴─────┘,
        ('b',): shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ b   ┆ 2   ┆ 4   │
        │ b   ┆ 3   ┆ 2   │
        └─────┴─────┴─────┘,
        ('c',): shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ c   ┆ 3   ┆ 1   │
        └─────┴─────┴─────┘}
        """
        by_parsed = _expand_selectors(self, by, *more_by)

        partitions = [
            self._from_pydf(_df)
            for _df in self._df.partition_by(by_parsed, maintain_order, include_key)
        ]

        if as_dict:
            if include_key:
                names = [p.select(by_parsed).row(0) for p in partitions]
            else:
                if not maintain_order:  # Group keys cannot be matched to partitions
                    msg = "cannot use `partition_by` with `maintain_order=False, include_key=False, as_dict=True`"
                    raise ValueError(msg)
                names = self.select(by_parsed).unique(maintain_order=True).rows()

            return dict(zip(names, partitions))

        return partitions
