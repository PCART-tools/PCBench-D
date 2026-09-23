def concat(
    items: Iterable[PolarsType],
    *,
    how: ConcatMethod = "vertical",
    rechunk: bool = False,
    parallel: bool = True,
) -> PolarsType:
    """
    Combine multiple DataFrames, LazyFrames, or Series into a single object.

    Parameters
    ----------
    items
        DataFrames, LazyFrames, or Series to concatenate.
    how : {'vertical', 'vertical_relaxed', 'diagonal', 'diagonal_relaxed', 'horizontal', 'align'}
        Series only support the `vertical` strategy.

        * vertical: Applies multiple `vstack` operations.
        * vertical_relaxed: Same as `vertical`, but additionally coerces columns to
          their common supertype *if* they are mismatched (eg: Int32 → Int64).
        * diagonal: Finds a union between the column schemas and fills missing column
          values with `null`.
        * diagonal_relaxed: Same as `diagonal`, but additionally coerces columns to
          their common supertype *if* they are mismatched (eg: Int32 → Int64).
        * horizontal: Stacks Series from DataFrames horizontally and fills with `null`
          if the lengths don't match.
        * align: Combines frames horizontally, auto-determining the common key columns
          and aligning rows using the same logic as `align_frames`; this behaviour is
          patterned after a full outer join, but does not handle column-name collision.
          (If you need more control, you should use a suitable join method instead).
    rechunk
        Make sure that the result data is in contiguous memory.
    parallel
        Only relevant for LazyFrames. This determines if the concatenated
        lazy computations may be executed in parallel.

    Examples
    --------
    >>> df1 = pl.DataFrame({"a": [1], "b": [3]})
    >>> df2 = pl.DataFrame({"a": [2], "b": [4]})
    >>> pl.concat([df1, df2])  # default is 'vertical' strategy
    shape: (2, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 3   │
    │ 2   ┆ 4   │
    └─────┴─────┘

    >>> df1 = pl.DataFrame({"a": [1], "b": [3]})
    >>> df2 = pl.DataFrame({"a": [2.5], "b": [4]})
    >>> pl.concat([df1, df2], how="vertical_relaxed")  # 'a' coerced into f64
    shape: (2, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ f64 ┆ i64 │
    ╞═════╪═════╡
    │ 1.0 ┆ 3   │
    │ 2.5 ┆ 4   │
    └─────┴─────┘

    >>> df_h1 = pl.DataFrame({"l1": [1, 2], "l2": [3, 4]})
    >>> df_h2 = pl.DataFrame({"r1": [5, 6], "r2": [7, 8], "r3": [9, 10]})
    >>> pl.concat([df_h1, df_h2], how="horizontal")
    shape: (2, 5)
    ┌─────┬─────┬─────┬─────┬─────┐
    │ l1  ┆ l2  ┆ r1  ┆ r2  ┆ r3  │
    │ --- ┆ --- ┆ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╪═════╡
    │ 1   ┆ 3   ┆ 5   ┆ 7   ┆ 9   │
    │ 2   ┆ 4   ┆ 6   ┆ 8   ┆ 10  │
    └─────┴─────┴─────┴─────┴─────┘

    >>> df_d1 = pl.DataFrame({"a": [1], "b": [3]})
    >>> df_d2 = pl.DataFrame({"a": [2], "c": [4]})
    >>> pl.concat([df_d1, df_d2], how="diagonal")
    shape: (2, 3)
    ┌─────┬──────┬──────┐
    │ a   ┆ b    ┆ c    │
    │ --- ┆ ---  ┆ ---  │
    │ i64 ┆ i64  ┆ i64  │
    ╞═════╪══════╪══════╡
    │ 1   ┆ 3    ┆ null │
    │ 2   ┆ null ┆ 4    │
    └─────┴──────┴──────┘

    >>> df_a1 = pl.DataFrame({"id": [1, 2], "x": [3, 4]})
    >>> df_a2 = pl.DataFrame({"id": [2, 3], "y": [5, 6]})
    >>> df_a3 = pl.DataFrame({"id": [1, 3], "z": [7, 8]})
    >>> pl.concat([df_a1, df_a2, df_a3], how="align")
    shape: (3, 4)
    ┌─────┬──────┬──────┬──────┐
    │ id  ┆ x    ┆ y    ┆ z    │
    │ --- ┆ ---  ┆ ---  ┆ ---  │
    │ i64 ┆ i64  ┆ i64  ┆ i64  │
    ╞═════╪══════╪══════╪══════╡
    │ 1   ┆ 3    ┆ null ┆ 7    │
    │ 2   ┆ 4    ┆ 5    ┆ null │
    │ 3   ┆ null ┆ 6    ┆ 8    │
    └─────┴──────┴──────┴──────┘
    """  # noqa: W505
    # unpack/standardise (handles generator input)
    elems = list(items)

    if not elems:
        msg = "cannot concat empty list"
        raise ValueError(msg)
    elif len(elems) == 1 and isinstance(
        elems[0], (pl.DataFrame, pl.Series, pl.LazyFrame)
    ):
        return elems[0]

    if how == "align":
        if not isinstance(elems[0], (pl.DataFrame, pl.LazyFrame)):
            msg = f"'align' strategy is not supported for {type(elems[0]).__name__!r}"
            raise TypeError(msg)

        # establish common columns, maintaining the order in which they appear
        all_columns = list(chain.from_iterable(e.collect_schema() for e in elems))
        key = {v: k for k, v in enumerate(ordered_unique(all_columns))}
        common_cols = sorted(
            reduce(
                lambda x, y: set(x) & set(y),  # type: ignore[arg-type, return-value]
                chain(e.collect_schema() for e in elems),
            ),
            key=lambda k: key.get(k, 0),
        )
        # we require at least one key column for 'align'
        if not common_cols:
            msg = "'align' strategy requires at least one common column"
            raise InvalidOperationError(msg)

        # align the frame data using a full outer join with no suffix-resolution
        # (so we raise an error in case of column collision, like "horizontal")
        lf: LazyFrame = reduce(
            lambda x, y: (
                x.join(y, how="full", on=common_cols, suffix="_PL_CONCAT_RIGHT")
                # Coalesce full outer join columns
                .with_columns(
                    F.coalesce([name, f"{name}_PL_CONCAT_RIGHT"])
                    for name in common_cols
                )
                .drop([f"{name}_PL_CONCAT_RIGHT" for name in common_cols])
            ),
            [df.lazy() for df in elems],
        ).sort(by=common_cols)

        eager = isinstance(elems[0], pl.DataFrame)
        return lf.collect() if eager else lf  # type: ignore[return-value]

    out: Series | DataFrame | LazyFrame | Expr
    first = elems[0]

    if isinstance(first, pl.DataFrame):
        if how == "vertical":
            out = wrap_df(plr.concat_df(elems))
        elif how == "vertical_relaxed":
            out = wrap_ldf(
                plr.concat_lf(
                    [df.lazy() for df in elems],
                    rechunk=rechunk,
                    parallel=parallel,
                    to_supertypes=True,
                )
            ).collect(no_optimization=True)

        elif how == "diagonal":
            out = wrap_df(plr.concat_df_diagonal(elems))
        elif how == "diagonal_relaxed":
            out = wrap_ldf(
                plr.concat_lf_diagonal(
                    [df.lazy() for df in elems],
                    rechunk=rechunk,
                    parallel=parallel,
                    to_supertypes=True,
                )
            ).collect(no_optimization=True)
        elif how == "horizontal":
            out = wrap_df(plr.concat_df_horizontal(elems))
        else:
            allowed = ", ".join(repr(m) for m in get_args(ConcatMethod))
            msg = f"DataFrame `how` must be one of {{{allowed}}}, got {how!r}"
            raise ValueError(msg)

    elif isinstance(first, pl.LazyFrame):
        if how in ("vertical", "vertical_relaxed"):
            return wrap_ldf(
                plr.concat_lf(
                    elems,
                    rechunk=rechunk,
                    parallel=parallel,
                    to_supertypes=how.endswith("relaxed"),
                )
            )
        elif how in ("diagonal", "diagonal_relaxed"):
            return wrap_ldf(
                plr.concat_lf_diagonal(
                    elems,
                    rechunk=rechunk,
                    parallel=parallel,
                    to_supertypes=how.endswith("relaxed"),
                )
            )
        elif how == "horizontal":
            return wrap_ldf(
                plr.concat_lf_horizontal(
                    elems,
                    parallel=parallel,
                )
            )
        else:
            allowed = ", ".join(repr(m) for m in get_args(ConcatMethod))
            msg = f"LazyFrame `how` must be one of {{{allowed}}}, got {how!r}"
            raise ValueError(msg)

    elif isinstance(first, pl.Series):
        if how == "vertical":
            out = wrap_s(plr.concat_series(elems))
        else:
            msg = "Series only supports 'vertical' concat strategy"
            raise ValueError(msg)

    elif isinstance(first, pl.Expr):
        return wrap_expr(plr.concat_expr([e._pyexpr for e in elems], rechunk))
    else:
        msg = f"did not expect type: {type(first).__name__!r} in `concat`"
        raise TypeError(msg)

    if rechunk:
        return out.rechunk()
    return out
