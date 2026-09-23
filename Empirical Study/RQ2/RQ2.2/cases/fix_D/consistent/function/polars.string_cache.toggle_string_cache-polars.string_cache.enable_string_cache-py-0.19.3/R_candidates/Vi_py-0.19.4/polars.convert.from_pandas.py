def from_pandas(
    data: pd.DataFrame | pd.Series[Any] | pd.Index[Any],
    *,
    schema_overrides: SchemaDict | None = None,
    rechunk: bool = True,
    nan_to_null: bool = True,
    include_index: bool = False,
) -> DataFrame | Series:
    """
    Construct a Polars DataFrame or Series from a pandas DataFrame or Series.

    This operation clones data.

    This requires that :mod:`pandas` and :mod:`pyarrow` are installed.

    Parameters
    ----------
    data : :class:`pandas.DataFrame` or :class:`pandas.Series` or :class:`pandas.Index`
        Data represented as a pandas DataFrame, Series, or Index.
    schema_overrides : dict, default None
        Support override of inferred types for one or more columns.
    rechunk : bool, default True
        Make sure that all data is in contiguous memory.
    nan_to_null : bool, default True
        If data contains `NaN` values PyArrow will convert the ``NaN`` to ``None``
    include_index : bool, default False
        Load any non-default pandas indexes as columns.

    Returns
    -------
    DataFrame

    Examples
    --------
    Constructing a :class:`DataFrame` from a :class:`pandas.DataFrame`:

    >>> import pandas as pd
    >>> pd_df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["a", "b", "c"])
    >>> df = pl.from_pandas(pd_df)
    >>> df
        shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 1   ┆ 2   ┆ 3   │
    │ 4   ┆ 5   ┆ 6   │
    └─────┴─────┴─────┘

    Constructing a Series from a :class:`pd.Series`:

    >>> import pandas as pd
    >>> pd_series = pd.Series([1, 2, 3], name="pd")
    >>> df = pl.from_pandas(pd_series)
    >>> df
    shape: (3,)
    Series: 'pd' [i64]
    [
        1
        2
        3
    ]

    """
    if isinstance(data, (pd.Series, pd.DatetimeIndex)):
        return pl.Series._from_pandas("", data, nan_to_null=nan_to_null)
    elif isinstance(data, pd.DataFrame):
        return pl.DataFrame._from_pandas(
            data,
            rechunk=rechunk,
            nan_to_null=nan_to_null,
            schema_overrides=schema_overrides,
            include_index=include_index,
        )
    else:
        raise TypeError(
            f"expected pandas DataFrame or Series, got {type(data).__name__!r}"
        )
