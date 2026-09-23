def map_groups(
    exprs: Sequence[str | Expr],
    function: Callable[[Sequence[Series]], Series | Any],
    return_dtype: PolarsDataType | None = None,
    *,
    returns_scalar: bool = True,
) -> Expr:
    """
    Apply a custom/user-defined function (UDF) in a GroupBy context.

    .. warning::
        This method is much slower than the native expressions API.
        Only use it if you cannot implement your logic otherwise.

    Parameters
    ----------
    exprs
        Expression(s) representing the input Series to the function.
    function
        Function to apply over the input; should be of type Callable[[Series], Series].
    return_dtype
        dtype of the output Series.
    returns_scalar
        If the function returns a single scalar as output.

    Returns
    -------
    Expr
        Expression with the data type given by `return_dtype`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "group": [1, 1, 2],
    ...         "a": [1, 3, 3],
    ...         "b": [5, 6, 7],
    ...     }
    ... )
    >>> df
    shape: (3, 3)
    ┌───────┬─────┬─────┐
    │ group ┆ a   ┆ b   │
    │ ---   ┆ --- ┆ --- │
    │ i64   ┆ i64 ┆ i64 │
    ╞═══════╪═════╪═════╡
    │ 1     ┆ 1   ┆ 5   │
    │ 1     ┆ 3   ┆ 6   │
    │ 2     ┆ 3   ┆ 7   │
    └───────┴─────┴─────┘
    >>> (
    ...     df.group_by("group").agg(
    ...         pl.map_groups(
    ...             exprs=["a", "b"],
    ...             function=lambda list_of_series: list_of_series[0]
    ...             / list_of_series[0].sum()
    ...             + list_of_series[1],
    ...         ).alias("my_custom_aggregation")
    ...     )
    ... ).sort("group")
    shape: (2, 2)
    ┌───────┬───────────────────────┐
    │ group ┆ my_custom_aggregation │
    │ ---   ┆ ---                   │
    │ i64   ┆ list[f64]             │
    ╞═══════╪═══════════════════════╡
    │ 1     ┆ [5.25, 6.75]          │
    │ 2     ┆ [8.0]                 │
    └───────┴───────────────────────┘

    The output for group `1` can be understood as follows:

    - group `1` contains Series `'a': [1, 3]` and `'b': [4, 5]`
    - applying the function to those lists of Series, one gets the output
      `[1 / 4 + 5, 3 / 4 + 6]`, i.e. `[5.25, 6.75]`
    """
    exprs = parse_into_list_of_expressions(exprs)
    return wrap_expr(
        plr.map_mul(
            exprs,
            function,
            return_dtype,
            map_groups=True,
            returns_scalar=returns_scalar,
        )
    )
