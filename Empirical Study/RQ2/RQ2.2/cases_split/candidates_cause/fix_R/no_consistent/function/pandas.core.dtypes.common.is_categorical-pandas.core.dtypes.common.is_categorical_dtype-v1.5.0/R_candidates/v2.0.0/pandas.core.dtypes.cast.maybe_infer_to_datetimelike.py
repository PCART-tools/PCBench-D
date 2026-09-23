def maybe_infer_to_datetimelike(
    value: npt.NDArray[np.object_],
) -> np.ndarray | DatetimeArray | TimedeltaArray | PeriodArray | IntervalArray:
    """
    we might have a array (or single object) that is datetime like,
    and no dtype is passed don't change the value unless we find a
    datetime/timedelta set

    this is pretty strict in that a datetime/timedelta is REQUIRED
    in addition to possible nulls/string likes

    Parameters
    ----------
    value : np.ndarray[object]

    Returns
    -------
    np.ndarray, DatetimeArray, TimedeltaArray, PeriodArray, or IntervalArray

    """
    if not isinstance(value, np.ndarray) or value.dtype != object:
        # Caller is responsible for passing only ndarray[object]
        raise TypeError(type(value))  # pragma: no cover
    if value.ndim != 1:
        # Caller is responsible
        raise ValueError(value.ndim)  # pragma: no cover

    if not len(value):
        return value

    # error: Incompatible return value type (got "Union[ExtensionArray,
    # ndarray[Any, Any]]", expected "Union[ndarray[Any, Any], DatetimeArray,
    # TimedeltaArray, PeriodArray, IntervalArray]")
    return lib.maybe_convert_objects(  # type: ignore[return-value]
        value,
        # Here we do not convert numeric dtypes, as if we wanted that,
        #  numpy would have done it for us.
        convert_numeric=False,
        convert_period=True,
        convert_interval=True,
        convert_timedelta=True,
        convert_datetime=True,
        dtype_if_all_nat=np.dtype("M8[ns]"),
    )
