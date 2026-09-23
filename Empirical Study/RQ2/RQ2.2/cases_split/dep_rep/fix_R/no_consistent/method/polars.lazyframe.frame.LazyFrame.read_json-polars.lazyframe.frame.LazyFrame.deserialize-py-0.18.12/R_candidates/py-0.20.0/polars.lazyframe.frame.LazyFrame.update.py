    def update(
        self,
        other: LazyFrame,
        on: str | Sequence[str] | None = None,
        how: Literal["left", "inner", "outer"] = "left",
        *,
        left_on: str | Sequence[str] | None = None,
        right_on: str | Sequence[str] | None = None,
        include_nulls: bool = False,
    ) -> Self:
        """
        Update the values in this `LazyFrame` with the non-null values in `other`.

        .. warning::
            This functionality is experimental and may change without it being
            considered a breaking change.

        Parameters
        ----------
        other
            LazyFrame that will be used to update the values
        on
            Column names that will be joined on; if given `None` the implicit row
            index is used as a join key instead.
        how : {'left', 'inner', 'outer'}
            * 'left' will keep all rows from the left table; rows may be duplicated
              if multiple rows in the right frame match the left row's key.
            * 'inner' keeps only those rows where the key exists in both frames.
            * 'outer' will update existing rows where the key matches while also
              adding any new rows contained in the given frame.
        left_on
           Join column(s) of the left DataFrame.
        right_on
           Join column(s) of the right DataFrame.
        include_nulls
            If True, null values from the right DataFrame will be used to update the
            left DataFrame.

        Notes
        -----
        This is syntactic sugar for a left/inner join, with an optional coalesce when
        `include_nulls = False`.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "A": [1, 2, 3, 4],
        ...         "B": [400, 500, 600, 700],
        ...     }
        ... )
        >>> lf.collect()
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
        >>> new_lf = pl.LazyFrame(
        ...     {
        ...         "B": [-66, None, -99],
        ...         "C": [5, 3, 1],
        ...     }
        ... )

        Update `df` values with the non-null values in `new_df`, by row index:

        >>> lf.update(new_lf).collect()
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

        >>> lf.update(new_lf, how="inner").collect()
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

        Update `df` values with the non-null values in `new_df`, using an outer join
        strategy that defines explicit join columns in each frame:

        >>> lf.update(new_lf, left_on=["A"], right_on=["C"], how="outer").collect()
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

        Update `df` values including null values in `new_df`, using an outer join
        strategy that defines explicit join columns in each frame:

        >>> lf.update(
        ...     new_lf, left_on="A", right_on="C", how="outer", include_nulls=True
        ... ).collect()
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
        if how not in ("left", "inner", "outer"):
            raise ValueError(
                f"`how` must be one of {{'left', 'inner', 'outer'}}; found {how!r}"
            )
        if how == "outer":
            how = "outer_coalesce"  # type: ignore[assignment]

        row_count_used = False
        if on is None:
            if left_on is None and right_on is None:
                # no keys provided--use row count
                row_count_used = True
                row_count_name = "__POLARS_ROW_COUNT"
                self = self.with_row_count(row_count_name)
                other = other.with_row_count(row_count_name)
                left_on = right_on = [row_count_name]
            else:
                # one of left or right is missing, raise error
                if left_on is None:
                    raise ValueError("missing join columns for left frame")
                if right_on is None:
                    raise ValueError("missing join columns for right frame")
        else:
            # move on into left/right_on to simplify logic
            left_on = right_on = on

        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        left_names = self.columns
        for name in left_on:
            if name not in left_names:
                raise ValueError(f"left join column {name!r} not found")
        right_names = other.columns
        for name in right_on:
            if name not in right_names:
                raise ValueError(f"right join column {name!r} not found")

        # no need to join if *only* join columns are in other (inner/left update only)
        if how != "outer_coalesce" and len(other.columns) == len(right_on):  # type: ignore[comparison-overlap, redundant-expr]
            if row_count_used:
                return self.drop(row_count_name)
            return self

        # only use non-idx right columns present in left frame
        right_other = set(other.columns).intersection(self.columns) - set(right_on)

        # When include_nulls is True, we need to distinguish records after the join that
        # were originally null in the right frame, as opposed to records that were null
        # because the key was missing from the right frame.
        # Add a validity column to track whether row was matched or not.
        if include_nulls:
            validity = ("__POLARS_VALIDITY",)
            other = other.with_columns(F.lit(True).alias(validity[0]))
        else:
            validity = ()  # type: ignore[assignment]

        tmp_name = "__POLARS_RIGHT"
        drop_columns = [*(f"{name}{tmp_name}" for name in right_other), *validity]
        result = (
            self.join(
                other.select(*right_on, *right_other, *validity),
                left_on=left_on,
                right_on=right_on,
                how=how,
                suffix=tmp_name,
            )
            .with_columns(
                (
                    # use left value only when right value failed to join
                    F.when(F.col(validity).is_null())
                    .then(F.col(name))
                    .otherwise(F.col(f"{name}{tmp_name}"))
                    if include_nulls
                    else F.coalesce([f"{name}{tmp_name}", F.col(name)])
                ).alias(name)
                for name in right_other
            )
            .drop(drop_columns)
        )
        if row_count_used:
            result = result.drop(row_count_name)

        return self._from_pyldf(result._ldf)
