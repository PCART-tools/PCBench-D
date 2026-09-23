    def transpose(
        self,
        *,
        include_header: bool = False,
        header_name: str = "column",
        column_names: str | Iterable[str] | None = None,
    ) -> DataFrame:
        """
        Transpose a DataFrame over the diagonal.

        Parameters
        ----------
        include_header
            If set, the column names will be added as first column.
        header_name
            If `include_header` is set, this determines the name of the column that will
            be inserted.
        column_names
            Optional iterable yielding strings or a string naming an existing column.
            These will name the value (non-header) columns in the transposed data.

        Notes
        -----
        This is a very expensive operation. Perhaps you can do it differently.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> df.transpose(include_header=True)
        shape: (2, 4)
        ┌────────┬──────────┬──────────┬──────────┐
        │ column ┆ column_0 ┆ column_1 ┆ column_2 │
        │ ---    ┆ ---      ┆ ---      ┆ ---      │
        │ str    ┆ i64      ┆ i64      ┆ i64      │
        ╞════════╪══════════╪══════════╪══════════╡
        │ a      ┆ 1        ┆ 2        ┆ 3        │
        │ b      ┆ 4        ┆ 5        ┆ 6        │
        └────────┴──────────┴──────────┴──────────┘

        Replace the auto-generated column names with a list

        >>> df.transpose(include_header=False, column_names=["x", "y", "z"])
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ x   ┆ y   ┆ z   │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 2   ┆ 3   │
        │ 4   ┆ 5   ┆ 6   │
        └─────┴─────┴─────┘

        Include the header as a separate column

        >>> df.transpose(
        ...     include_header=True, header_name="foo", column_names=["x", "y", "z"]
        ... )
        shape: (2, 4)
        ┌─────┬─────┬─────┬─────┐
        │ foo ┆ x   ┆ y   ┆ z   │
        │ --- ┆ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 2   ┆ 3   │
        │ b   ┆ 4   ┆ 5   ┆ 6   │
        └─────┴─────┴─────┴─────┘

        Replace the auto-generated column with column names from a generator function

        >>> def name_generator():
        ...     base_name = "my_column_"
        ...     count = 0
        ...     while True:
        ...         yield f"{base_name}{count}"
        ...         count += 1
        >>> df.transpose(include_header=False, column_names=name_generator())
        shape: (2, 3)
        ┌─────────────┬─────────────┬─────────────┐
        │ my_column_0 ┆ my_column_1 ┆ my_column_2 │
        │ ---         ┆ ---         ┆ ---         │
        │ i64         ┆ i64         ┆ i64         │
        ╞═════════════╪═════════════╪═════════════╡
        │ 1           ┆ 2           ┆ 3           │
        │ 4           ┆ 5           ┆ 6           │
        └─────────────┴─────────────┴─────────────┘

        Use an existing column as the new column names

        >>> df = pl.DataFrame(dict(id=["i", "j", "k"], a=[1, 2, 3], b=[4, 5, 6]))
        >>> df.transpose(column_names="id")
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ i   ┆ j   ┆ k   │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 2   ┆ 3   │
        │ 4   ┆ 5   ┆ 6   │
        └─────┴─────┴─────┘
        >>> df.transpose(include_header=True, header_name="new_id", column_names="id")
        shape: (2, 4)
        ┌────────┬─────┬─────┬─────┐
        │ new_id ┆ i   ┆ j   ┆ k   │
        │ ---    ┆ --- ┆ --- ┆ --- │
        │ str    ┆ i64 ┆ i64 ┆ i64 │
        ╞════════╪═════╪═════╪═════╡
        │ a      ┆ 1   ┆ 2   ┆ 3   │
        │ b      ┆ 4   ┆ 5   ┆ 6   │
        └────────┴─────┴─────┴─────┘
        """
        keep_names_as = header_name if include_header else None
        if isinstance(column_names, Generator):
            column_names = [next(column_names) for _ in range(self.height)]
        return self._from_pydf(self._df.transpose(keep_names_as, column_names))
