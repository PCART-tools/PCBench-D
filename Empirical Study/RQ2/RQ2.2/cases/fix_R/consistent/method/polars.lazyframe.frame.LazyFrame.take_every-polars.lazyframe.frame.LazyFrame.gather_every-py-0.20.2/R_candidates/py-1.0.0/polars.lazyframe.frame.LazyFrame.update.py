    @unstable()
    def update(
        self,
        other: LazyFrame,
        on: str | Sequence[str] | None = None,
        how: Literal["left", "inner", "full"] = "left",
        *,
        left_on: str | Sequence[str] | None = None,
        right_on: str | Sequence[str] | None = None,
        include_nulls: bool = False,
    ) -> LazyFrame:
        """
        Update the values in this `LazyFrame` with the values in `other`.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        other
            LazyFrame that will be used to update the values
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

        Update `df` values with the non-null values in `new_df`, using a full
        outer join strategy that defines explicit join columns in each frame:

        >>> lf.update(new_lf, left_on=["A"], right_on=["C"], how="full").collect()
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

        Update `df` values including null values in `new_df`, using a full
        outer join strategy that defines explicit join columns in each frame:

        >>> lf.update(
        ...     new_lf, left_on="A", right_on="C", how="full", include_nulls=True
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
        if how in ("outer", "outer_coalesce"):
            how = "full"
            issue_deprecation_warning(
                "Use of `how='outer'` should be replaced with `how='full'`.",
                version="0.20.29",
            )

        if how not in ("left", "inner", "full"):
            msg = f"`how` must be one of {{'left', 'inner', 'full'}}; found {how!r}"
            raise ValueError(msg)

        row_index_used = False
        if on is None:
            if left_on is None and right_on is None:
                # no keys provided--use row index
                row_index_used = True
                row_index_name = "__POLARS_ROW_INDEX"
                self = self.with_row_index(row_index_name)
                other = other.with_row_index(row_index_name)
                left_on = right_on = [row_index_name]
            else:
                # one of left or right is missing, raise error
                if left_on is None:
                    msg = "missing join columns for left frame"
                    raise ValueError(msg)
                if right_on is None:
                    msg = "missing join columns for right frame"
                    raise ValueError(msg)
        else:
            # move on into left/right_on to simplify logic
            left_on = right_on = on

        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        left_schema = self.collect_schema()
        for name in left_on:
            if name not in left_schema:
                msg = f"left join column {name!r} not found"
                raise ValueError(msg)
        right_schema = other.collect_schema()
        for name in right_on:
            if name not in right_schema:
                msg = f"right join column {name!r} not found"
                raise ValueError(msg)

        # no need to join if *only* join columns are in other (inner/left update only)
        if how != "full" and len(right_schema) == len(right_on):
            if row_index_used:
                return self.drop(row_index_name)
            return self

        # only use non-idx right columns present in left frame
        right_other = set(right_schema).intersection(left_schema) - set(right_on)

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
                coalesce=True,
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
        if row_index_used:
            result = result.drop(row_index_name)

        return self._from_pyldf(result._ldf)
