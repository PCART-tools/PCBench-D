    @unstable()
    def update(
        self,
        other: DataFrame,
        on: str | Sequence[str] | None = None,
        how: Literal["left", "inner", "full"] = "left",
        *,
        left_on: str | Sequence[str] | None = None,
        right_on: str | Sequence[str] | None = None,
        include_nulls: bool = False,
    ) -> DataFrame:
        """
        Update the values in this `DataFrame` with the values in `other`.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        other
            DataFrame that will be used to update the values
        on
            Column names that will be joined on. If set to `None` (default),
            the implicit row index of each frame is used as a join key.
        how : {'left', 'inner', 'full'}
            * 'left' will keep all rows from the left table; rows may be duplicated
              if multiple rows in the right frame match the left row's key.
            * 'inner' keeps only those rows where the key exists in both frames.
            * 'full' will update existing rows where the key matches while also
              adding any new rows contained in the given frame.
        left_on
           Join column(s) of the left DataFrame.
        right_on
           Join column(s) of the right DataFrame.
        include_nulls
            Overwrite values in the left frame with null values from the right frame.
            If set to `False` (default), null values in the right frame are ignored.

        Notes
        -----
        This is syntactic sugar for a left/inner join, with an optional coalesce
        when `include_nulls = False`

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "A": [1, 2, 3, 4],
        ...         "B": [400, 500, 600, 700],
        ...     }
        ... )
        >>> df
        shape: (4, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 400 │
        │ 2   ┆ 500 │
        │ 3   ┆ 600 │
        │ 4   ┆ 700 │
        └─────┴─────┘
        >>> new_df = pl.DataFrame(
        ...     {
        ...         "B": [-66, None, -99],
        ...         "C": [5, 3, 1],
        ...     }
        ... )

        Update `df` values with the non-null values in `new_df`, by row index:

        >>> df.update(new_df)
        shape: (4, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ -66 │
        │ 2   ┆ 500 │
        │ 3   ┆ -99 │
        │ 4   ┆ 700 │
        └─────┴─────┘

        Update `df` values with the non-null values in `new_df`, by row index,
        but only keeping those rows that are common to both frames:

        >>> df.update(new_df, how="inner")
        shape: (3, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ -66 │
        │ 2   ┆ 500 │
        │ 3   ┆ -99 │
        └─────┴─────┘

        Update `df` values with the non-null values in `new_df`, using a full
        outer join strategy that defines explicit join columns in each frame:

        >>> df.update(new_df, left_on=["A"], right_on=["C"], how="full")
        shape: (5, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ -99 │
        │ 2   ┆ 500 │
        │ 3   ┆ 600 │
        │ 4   ┆ 700 │
        │ 5   ┆ -66 │
        └─────┴─────┘

        Update `df` values including null values in `new_df`, using a full outer
        join strategy that defines explicit join columns in each frame:

        >>> df.update(new_df, left_on="A", right_on="C", how="full", include_nulls=True)
        shape: (5, 2)
        ┌─────┬──────┐
        │ A   ┆ B    │
        │ --- ┆ ---  │
        │ i64 ┆ i64  │
        ╞═════╪══════╡
        │ 1   ┆ -99  │
        │ 2   ┆ 500  │
        │ 3   ┆ null │
        │ 4   ┆ 700  │
        │ 5   ┆ -66  │
        └─────┴──────┘
        """
        return (
            self.lazy()
            .update(
                other.lazy(),
                on,
                how,
                left_on=left_on,
                right_on=right_on,
                include_nulls=include_nulls,
            )
            .collect(_eager=True)
        )
