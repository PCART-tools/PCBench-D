def _pandas_series_to_arrow(
    values: pd.Series[Any] | pd.Index[Any],
    *,
    length: int | None = None,
    nan_to_null: bool = True,
) -> pa.Array:
    """
    Convert a pandas Series to an Arrow Array.

    Parameters
    ----------
    values : :class:`pandas.Series` or :class:`pandas.Index`.
        Series to convert to arrow
    nan_to_null : bool, default = True
        Interpret `NaN` as missing values.
    length : int, optional
        in case all values are null, create a null array of this length.
        if unset, length is inferred from values.

    Returns
    -------
    :class:`pyarrow.Array`

    """
    dtype = getattr(values, "dtype", None)
    if dtype == "object":
        first_non_none = _get_first_non_none(values.values)  # type: ignore[arg-type]
        if isinstance(first_non_none, str):
            return pa.array(values, pa.large_utf8(), from_pandas=nan_to_null)
        elif first_non_none is None:
            return pa.nulls(length or len(values), pa.large_utf8())
        return pa.array(values, from_pandas=nan_to_null)
    elif dtype:
        return pa.array(values, from_pandas=nan_to_null)
    else:
        # Pandas Series is actually a Pandas DataFrame when the original dataframe
        # contains duplicated columns and a duplicated column is requested with df["a"].
        raise ValueError(
            "duplicate column names found: ",
            f"{values.columns.tolist()!s}",  # type: ignore[union-attr]
        )
