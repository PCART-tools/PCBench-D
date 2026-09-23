def maybe_unbox_datetimelike_tz_deprecation(
    value: Scalar, dtype: DtypeObj, stacklevel: int = 5
):
    """
    Wrap maybe_unbox_datetimelike with a check for a timezone-aware Timestamp
    along with a timezone-naive datetime64 dtype, which is deprecated.
    """
    # Caller is responsible for checking dtype.kind in ["m", "M"]

    if isinstance(value, datetime):
        # we dont want to box dt64, in particular datetime64("NaT")
        value = maybe_box_datetimelike(value, dtype)

    try:
        value = maybe_unbox_datetimelike(value, dtype)
    except TypeError:
        if (
            isinstance(value, Timestamp)
            and value.tzinfo is not None
            and isinstance(dtype, np.dtype)
            and dtype.kind == "M"
        ):
            warnings.warn(
                "Data is timezone-aware. Converting "
                "timezone-aware data to timezone-naive by "
                "passing dtype='datetime64[ns]' to "
                "DataFrame or Series is deprecated and will "
                "raise in a future version. Use "
                "`pd.Series(values).dt.tz_localize(None)` "
                "instead.",
                FutureWarning,
                stacklevel=stacklevel,
            )
            new_value = value.tz_localize(None)
            return maybe_unbox_datetimelike(new_value, dtype)
        else:
            raise
    return value
