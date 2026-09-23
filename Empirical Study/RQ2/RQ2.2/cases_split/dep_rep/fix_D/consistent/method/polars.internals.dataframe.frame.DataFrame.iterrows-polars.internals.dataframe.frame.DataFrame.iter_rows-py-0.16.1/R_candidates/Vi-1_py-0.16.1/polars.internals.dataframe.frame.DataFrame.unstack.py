    def unstack(
        self: DF,
        step: int,
        how: UnstackDirection = "vertical",
        columns: str | Sequence[str] | None = None,
        fill_values: list[Any] | None = None,
    ) -> DF:
        """
        Unstack a long table to a wide form without doing an aggregation.

        This can be much faster than a pivot, because it can skip the grouping phase.

        Warnings
        --------
        This functionality is experimental and may be subject to changes
        without it being considered a breaking change.

        Parameters
        ----------
        step
            Number of rows in the unstacked frame.
        how : { 'vertical', 'horizontal' }
            Direction of the unstack.
        columns
            Column to include in the operation.
        fill_values
            Fill values that don't fit the new size with this value.

        Examples
        --------
        >>> from string import ascii_uppercase
        >>> df = pl.DataFrame(
        ...     {
        ...         "col1": list(ascii_uppercase[0:9]),
        ...         "col2": pl.arange(0, 9, eager=True),
        ...     }
        ... )
        >>> df
        shape: (9, 2)
        ┌──────┬──────┐
        │ col1 ┆ col2 │
        │ ---  ┆ ---  │
        │ str  ┆ i64  │
        ╞══════╪══════╡
        │ A    ┆ 0    │
        │ B    ┆ 1    │
        │ C    ┆ 2    │
        │ D    ┆ 3    │
        │ ...  ┆ ...  │
        │ F    ┆ 5    │
        │ G    ┆ 6    │
        │ H    ┆ 7    │
        │ I    ┆ 8    │
        └──────┴──────┘
        >>> df.unstack(step=3, how="vertical")
        shape: (3, 6)
        ┌────────┬────────┬────────┬────────┬────────┬────────┐
        │ col1_0 ┆ col1_1 ┆ col1_2 ┆ col2_0 ┆ col2_1 ┆ col2_2 │
        │ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    │
        │ str    ┆ str    ┆ str    ┆ i64    ┆ i64    ┆ i64    │
        ╞════════╪════════╪════════╪════════╪════════╪════════╡
        │ A      ┆ D      ┆ G      ┆ 0      ┆ 3      ┆ 6      │
        │ B      ┆ E      ┆ H      ┆ 1      ┆ 4      ┆ 7      │
        │ C      ┆ F      ┆ I      ┆ 2      ┆ 5      ┆ 8      │
        └────────┴────────┴────────┴────────┴────────┴────────┘
        >>> df.unstack(step=3, how="horizontal")
        shape: (3, 6)
        ┌────────┬────────┬────────┬────────┬────────┬────────┐
        │ col1_0 ┆ col1_1 ┆ col1_2 ┆ col2_0 ┆ col2_1 ┆ col2_2 │
        │ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    │
        │ str    ┆ str    ┆ str    ┆ i64    ┆ i64    ┆ i64    │
        ╞════════╪════════╪════════╪════════╪════════╪════════╡
        │ A      ┆ B      ┆ C      ┆ 0      ┆ 1      ┆ 2      │
        │ D      ┆ E      ┆ F      ┆ 3      ┆ 4      ┆ 5      │
        │ G      ┆ H      ┆ I      ┆ 6      ┆ 7      ┆ 8      │
        └────────┴────────┴────────┴────────┴────────┴────────┘

        """
        if columns is not None:
            df = self.select(columns)
        else:
            df = self

        height = df.height
        if how == "vertical":
            n_rows = step
            n_cols = math.ceil(height / n_rows)
        else:
            n_cols = step
            n_rows = math.ceil(height / n_cols)

        n_fill = n_cols * n_rows - height

        if n_fill:
            if not isinstance(fill_values, list):
                fill_values = [fill_values for _ in range(0, df.width)]

            df = df.select(
                [
                    s.extend_constant(next_fill, n_fill)
                    for s, next_fill in zip(df, fill_values)
                ]
            )

        if how == "horizontal":
            df = (
                df.with_columns(  # type: ignore[assignment]
                    (pli.arange(0, n_cols * n_rows, eager=True) % n_cols).alias(
                        "__sort_order"
                    ),
                )
                .sort("__sort_order")
                .drop("__sort_order")
            )

        zfill_val = math.floor(math.log10(n_cols)) + 1
        slices = [
            s.slice(slice_nbr * n_rows, n_rows).alias(
                s.name + "_" + str(slice_nbr).zfill(zfill_val)
            )
            for s in df
            for slice_nbr in range(0, n_cols)
        ]

        return self._from_pydf(DataFrame(slices)._df)
