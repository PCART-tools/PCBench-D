    def partition_by(
        self: DF,
        groups: str | Sequence[str],
        *,
        maintain_order: bool = True,
        as_dict: bool = False,
    ) -> list[DF] | dict[Any, DF]:
        """
        Split into multiple DataFrames partitioned by groups.

        Parameters
        ----------
        groups
            Groups to partition by.
        maintain_order
            Keep predictable output order. This is slower as it requires an extra sort
            operation.
        as_dict
            If True, return the partitions in a dictionary keyed by the distinct group
            values instead of a list.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": ["A", "A", "B", "B", "C"],
        ...         "N": [1, 2, 2, 4, 2],
        ...         "bar": ["k", "l", "m", "m", "l"],
        ...     }
        ... )
        >>> df.partition_by(groups="foo", maintain_order=True)
        [shape: (2, 3)
         ┌─────┬─────┬─────┐
         │ foo ┆ N   ┆ bar │
         │ --- ┆ --- ┆ --- │
         │ str ┆ i64 ┆ str │
         ╞═════╪═════╪═════╡
         │ A   ┆ 1   ┆ k   │
         │ A   ┆ 2   ┆ l   │
         └─────┴─────┴─────┘,
         shape: (2, 3)
         ┌─────┬─────┬─────┐
         │ foo ┆ N   ┆ bar │
         │ --- ┆ --- ┆ --- │
         │ str ┆ i64 ┆ str │
         ╞═════╪═════╪═════╡
         │ B   ┆ 2   ┆ m   │
         │ B   ┆ 4   ┆ m   │
         └─────┴─────┴─────┘,
         shape: (1, 3)
         ┌─────┬─────┬─────┐
         │ foo ┆ N   ┆ bar │
         │ --- ┆ --- ┆ --- │
         │ str ┆ i64 ┆ str │
         ╞═════╪═════╪═════╡
         │ C   ┆ 2   ┆ l   │
         └─────┴─────┴─────┘]
        >>> df.partition_by(groups="foo", maintain_order=True, as_dict=True)
        {'A': shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ N   ┆ bar │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ A   ┆ 1   ┆ k   │
        │ A   ┆ 2   ┆ l   │
        └─────┴─────┴─────┘, 'B': shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ N   ┆ bar │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ B   ┆ 2   ┆ m   │
        │ B   ┆ 4   ┆ m   │
        └─────┴─────┴─────┘, 'C': shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ N   ┆ bar │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ C   ┆ 2   ┆ l   │
        └─────┴─────┴─────┘}

        """
        if isinstance(groups, str):
            groups = [groups]
        elif not isinstance(groups, list):
            groups = list(groups)

        if as_dict:
            out: dict[Any, DF] = {}
            if len(groups) == 1:
                for _df in self._df.partition_by(groups, maintain_order):
                    df = self._from_pydf(_df)
                    out[df[groups][0, 0]] = df
            else:
                for _df in self._df.partition_by(groups, maintain_order):
                    df = self._from_pydf(_df)
                    out[df[groups].row(0)] = df

            return out

        else:
            return [
                self._from_pydf(_df)
                for _df in self._df.partition_by(groups, maintain_order)
            ]
