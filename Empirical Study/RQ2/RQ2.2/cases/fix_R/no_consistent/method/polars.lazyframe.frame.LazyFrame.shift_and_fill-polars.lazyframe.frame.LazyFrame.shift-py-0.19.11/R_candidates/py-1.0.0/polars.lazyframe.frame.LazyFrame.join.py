    def join(
        self,
        other: LazyFrame,
        on: str | Expr | Sequence[str | Expr] | None = None,
        how: JoinStrategy = "inner",
        *,
        left_on: str | Expr | Sequence[str | Expr] | None = None,
        right_on: str | Expr | Sequence[str | Expr] | None = None,
        suffix: str = "_right",
        validate: JoinValidation = "m:m",
        join_nulls: bool = False,
        coalesce: bool | None = None,
        allow_parallel: bool = True,
        force_parallel: bool = False,
    ) -> LazyFrame:
        """
        Add a join operation to the Logical Plan.

        Parameters
        ----------
        other
            Lazy DataFrame to join with.
        on
            Join column of both DataFrames. If set, `left_on` and `right_on` should be
            None.
        how : {'inner', 'left', 'full', 'semi', 'anti', 'cross'}
            Join strategy.

            * *inner*
                Returns rows that have matching values in both tables
            * *left*
                Returns all rows from the left table, and the matched rows from the
                right table
            * *full*
                 Returns all rows when there is a match in either left or right table
            * *cross*
                 Returns the Cartesian product of rows from both tables
            * *semi*
                 Filter rows that have a match in the right table.
            * *anti*
                 Filter rows that not have a match in the right table.

            .. note::
                A left join preserves the row order of the left DataFrame.
        left_on
            Join column of the left DataFrame.
        right_on
            Join column of the right DataFrame.
        suffix
            Suffix to append to columns with a duplicate name.
        validate: {'m:m', 'm:1', '1:m', '1:1'}
            Checks if join is of specified type.

                * *many_to_many*
                    “m:m”: default, does not result in checks
                * *one_to_one*
                    “1:1”: check if join keys are unique in both left and right datasets
                * *one_to_many*
                    “1:m”: check if join keys are unique in left dataset
                * *many_to_one*
                    “m:1”: check if join keys are unique in right dataset

            .. note::
                This is currently not supported by the streaming engine.

        join_nulls
            Join on null values. By default null values will never produce matches.
        coalesce
            Coalescing behavior (merging of join columns).

            - None: -> join specific.
            - True: -> Always coalesce join columns.
            - False: -> Never coalesce join columns.

            Note that joining on any other expressions than `col`
            will turn off coalescing.
        allow_parallel
            Allow the physical plan to optionally evaluate the computation of both
            DataFrames up to the join in parallel.
        force_parallel
            Force the physical plan to evaluate the computation of both DataFrames up to
            the join in parallel.

        See Also
        --------
        join_asof

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> other_lf = pl.LazyFrame(
        ...     {
        ...         "apple": ["x", "y", "z"],
        ...         "ham": ["a", "b", "d"],
        ...     }
        ... )
        >>> lf.join(other_lf, on="ham").collect()
        shape: (2, 4)
        ┌─────┬─────┬─────┬───────┐
        │ foo ┆ bar ┆ ham ┆ apple │
        │ --- ┆ --- ┆ --- ┆ ---   │
        │ i64 ┆ f64 ┆ str ┆ str   │
        ╞═════╪═════╪═════╪═══════╡
        │ 1   ┆ 6.0 ┆ a   ┆ x     │
        │ 2   ┆ 7.0 ┆ b   ┆ y     │
        └─────┴─────┴─────┴───────┘
        >>> lf.join(other_lf, on="ham", how="full").collect()
        shape: (4, 5)
        ┌──────┬──────┬──────┬───────┬───────────┐
        │ foo  ┆ bar  ┆ ham  ┆ apple ┆ ham_right │
        │ ---  ┆ ---  ┆ ---  ┆ ---   ┆ ---       │
        │ i64  ┆ f64  ┆ str  ┆ str   ┆ str       │
        ╞══════╪══════╪══════╪═══════╪═══════════╡
        │ 1    ┆ 6.0  ┆ a    ┆ x     ┆ a         │
        │ 2    ┆ 7.0  ┆ b    ┆ y     ┆ b         │
        │ null ┆ null ┆ null ┆ z     ┆ d         │
        │ 3    ┆ 8.0  ┆ c    ┆ null  ┆ null      │
        └──────┴──────┴──────┴───────┴───────────┘
        >>> lf.join(other_lf, on="ham", how="left", coalesce=True).collect()
        shape: (3, 4)
        ┌─────┬─────┬─────┬───────┐
        │ foo ┆ bar ┆ ham ┆ apple │
        │ --- ┆ --- ┆ --- ┆ ---   │
        │ i64 ┆ f64 ┆ str ┆ str   │
        ╞═════╪═════╪═════╪═══════╡
        │ 1   ┆ 6.0 ┆ a   ┆ x     │
        │ 2   ┆ 7.0 ┆ b   ┆ y     │
        │ 3   ┆ 8.0 ┆ c   ┆ null  │
        └─────┴─────┴─────┴───────┘
        >>> lf.join(other_lf, on="ham", how="semi").collect()
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ f64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6.0 ┆ a   │
        │ 2   ┆ 7.0 ┆ b   │
        └─────┴─────┴─────┘
        >>> lf.join(other_lf, on="ham", how="anti").collect()
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ f64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 3   ┆ 8.0 ┆ c   │
        └─────┴─────┴─────┘
        """
        if not isinstance(other, LazyFrame):
            msg = f"expected `other` join table to be a LazyFrame, not a {type(other).__name__!r}"
            raise TypeError(msg)

        if how == "outer":
            how = "full"
            issue_deprecation_warning(
                "Use of `how='outer'` should be replaced with `how='full'`.",
                version="0.20.29",
            )
        elif how == "outer_coalesce":  # type: ignore[comparison-overlap]
            coalesce = True
            how = "full"
            issue_deprecation_warning(
                "Use of `how='outer_coalesce'` should be replaced with `how='full', coalesce=True`.",
                version="0.20.29",
            )

        elif how == "cross":
            if left_on is not None or right_on is not None:
                msg = "cross join should not pass join keys"
                raise ValueError(msg)
            return self._from_pyldf(
                self._ldf.join(
                    other._ldf,
                    [],
                    [],
                    allow_parallel,
                    force_parallel,
                    join_nulls,
                    how,
                    suffix,
                    validate,
                )
            )

        if on is not None:
            pyexprs = parse_into_list_of_expressions(on)
            pyexprs_left = pyexprs
            pyexprs_right = pyexprs
        elif left_on is not None and right_on is not None:
            pyexprs_left = parse_into_list_of_expressions(left_on)
            pyexprs_right = parse_into_list_of_expressions(right_on)
        else:
            msg = "must specify `on` OR `left_on` and `right_on`"
            raise ValueError(msg)

        return self._from_pyldf(
            self._ldf.join(
                other._ldf,
                pyexprs_left,
                pyexprs_right,
                allow_parallel,
                force_parallel,
                join_nulls,
                how,
                suffix,
                validate,
                coalesce,
            )
        )
