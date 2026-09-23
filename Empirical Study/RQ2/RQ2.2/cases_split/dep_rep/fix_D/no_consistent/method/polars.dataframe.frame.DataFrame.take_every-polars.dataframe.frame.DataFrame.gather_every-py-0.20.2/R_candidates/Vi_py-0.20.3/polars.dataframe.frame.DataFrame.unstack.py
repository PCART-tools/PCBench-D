    def unstack(
        self,
        step: int,
        how: UnstackDirection = "vertical",
        columns: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        fill_values: list[Any] | None = None,
    ) -> DataFrame:
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
            Column name(s) or selector(s) to include in the operation.
            If set to `None` (default), use all columns.
        fill_values
            Fill values that don't fit the new size with this value.

        Examples
        --------
        >>> from string import ascii_uppercase
        >>> df = pl.DataFrame(
        ...     {
        ...         "x": list(ascii_uppercase[0:8]),
        ...         "y": pl.int_range(1, 9, eager=True),
        ...     }
        ... ).with_columns(
        ...     z=pl.int_ranges(pl.col("y"), pl.col("y") + 2, dtype=pl.UInt8),
        ... )
        >>> df
        shape: (8, 3)
        ┌─────┬─────┬──────────┐
        │ x   ┆ y   ┆ z        │
        │ --- ┆ --- ┆ ---      │
        │ str ┆ i64 ┆ list[u8] │
        ╞═════╪═════╪══════════╡
        │ A   ┆ 1   ┆ [1, 2]   │
        │ B   ┆ 2   ┆ [2, 3]   │
        │ C   ┆ 3   ┆ [3, 4]   │
        │ D   ┆ 4   ┆ [4, 5]   │
        │ E   ┆ 5   ┆ [5, 6]   │
        │ F   ┆ 6   ┆ [6, 7]   │
        │ G   ┆ 7   ┆ [7, 8]   │
        │ H   ┆ 8   ┆ [8, 9]   │
        └─────┴─────┴──────────┘
        >>> df.unstack(step=4, how="vertical")
        shape: (4, 6)
        ┌─────┬─────┬─────┬─────┬──────────┬──────────┐
        │ x_0 ┆ x_1 ┆ y_0 ┆ y_1 ┆ z_0      ┆ z_1      │
        │ --- ┆ --- ┆ --- ┆ --- ┆ ---      ┆ ---      │
        │ str ┆ str ┆ i64 ┆ i64 ┆ list[u8] ┆ list[u8] │
        ╞═════╪═════╪═════╪═════╪══════════╪══════════╡
        │ A   ┆ E   ┆ 1   ┆ 5   ┆ [1, 2]   ┆ [5, 6]   │
        │ B   ┆ F   ┆ 2   ┆ 6   ┆ [2, 3]   ┆ [6, 7]   │
        │ C   ┆ G   ┆ 3   ┆ 7   ┆ [3, 4]   ┆ [7, 8]   │
        │ D   ┆ H   ┆ 4   ┆ 8   ┆ [4, 5]   ┆ [8, 9]   │
        └─────┴─────┴─────┴─────┴──────────┴──────────┘
        >>> df.unstack(step=2, how="horizontal")
        shape: (4, 6)
        ┌─────┬─────┬─────┬─────┬──────────┬──────────┐
        │ x_0 ┆ x_1 ┆ y_0 ┆ y_1 ┆ z_0      ┆ z_1      │
        │ --- ┆ --- ┆ --- ┆ --- ┆ ---      ┆ ---      │
        │ str ┆ str ┆ i64 ┆ i64 ┆ list[u8] ┆ list[u8] │
        ╞═════╪═════╪═════╪═════╪══════════╪══════════╡
        │ A   ┆ B   ┆ 1   ┆ 2   ┆ [1, 2]   ┆ [2, 3]   │
        │ C   ┆ D   ┆ 3   ┆ 4   ┆ [3, 4]   ┆ [4, 5]   │
        │ E   ┆ F   ┆ 5   ┆ 6   ┆ [5, 6]   ┆ [6, 7]   │
        │ G   ┆ H   ┆ 7   ┆ 8   ┆ [7, 8]   ┆ [8, 9]   │
        └─────┴─────┴─────┴─────┴──────────┴──────────┘
        >>> import polars.selectors as cs
        >>> df.unstack(step=5, columns=cs.numeric(), fill_values=0)
        shape: (5, 2)
        ┌─────┬─────┐
        │ y_0 ┆ y_1 │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 6   │
        │ 2   ┆ 7   │
        │ 3   ┆ 8   │
        │ 4   ┆ 0   │
        │ 5   ┆ 0   │
        └─────┴─────┘

        """
        import math

        df = self.select(columns) if columns is not None else self

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
                fill_values = [fill_values for _ in range(df.width)]

            df = df.select(
                [
                    s.extend_constant(next_fill, n_fill)
                    for s, next_fill in zip(df, fill_values)
                ]
            )

        if how == "horizontal":
            df = (
                df.with_columns(
                    (F.int_range(0, n_cols * n_rows, eager=True) % n_cols).alias(
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
            for slice_nbr in range(n_cols)
        ]

        return DataFrame(slices)
