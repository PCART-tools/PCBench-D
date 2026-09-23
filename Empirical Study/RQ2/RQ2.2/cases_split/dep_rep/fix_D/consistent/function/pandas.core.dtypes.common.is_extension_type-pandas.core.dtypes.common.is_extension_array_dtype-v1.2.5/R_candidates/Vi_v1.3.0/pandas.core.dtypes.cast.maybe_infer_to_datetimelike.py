def maybe_infer_to_datetimelike(
    value: np.ndarray,
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

    v = np.array(value, copy=False)

    shape = v.shape
    if v.ndim != 1:
        v = v.ravel()

    if not len(v):
        return value

    def try_datetime(v: np.ndarray) -> ArrayLike:
        # Coerce to datetime64, datetime64tz, or in corner cases
        #  object[datetimes]
        from pandas.core.arrays.datetimes import sequence_to_datetimes

        try:
            # GH#19671 we pass require_iso8601 to be relatively strict
            #  when parsing strings.
            dta = sequence_to_datetimes(v, require_iso8601=True, allow_object=True)
        except (ValueError, TypeError):
            # e.g. <class 'numpy.timedelta64'> is not convertible to datetime
            return v.reshape(shape)
        else:
            # GH#19761 we may have mixed timezones, in which cast 'dta' is
            #  an ndarray[object].  Only 1 test
            #  relies on this behavior, see GH#40111
            return dta.reshape(shape)

    def try_timedelta(v: np.ndarray) -> np.ndarray:
        # safe coerce to timedelta64

        # will try first with a string & object conversion
        try:
            # bc we know v.dtype == object, this is equivalent to
            #  `np.asarray(to_timedelta(v))`, but using a lower-level API that
            #  does not require a circular import.
            td_values = array_to_timedelta64(v).view("m8[ns]")
        except (ValueError, OverflowError):
            return v.reshape(shape)
        else:
            return td_values.reshape(shape)

    inferred_type, seen_str = lib.infer_datetimelike_array(ensure_object(v))
    if inferred_type in ["period", "interval"]:
        # Incompatible return value type (got "Union[ExtensionArray, ndarray]",
        # expected "Union[ndarray, DatetimeArray, TimedeltaArray, PeriodArray,
        # IntervalArray]")
        return lib.maybe_convert_objects(  # type: ignore[return-value]
            v, convert_period=True, convert_interval=True
        )

    if inferred_type == "datetime":
        # error: Incompatible types in assignment (expression has type "ExtensionArray",
        # variable has type "Union[ndarray, List[Any]]")
        value = try_datetime(v)  # type: ignore[assignment]
    elif inferred_type == "timedelta":
        value = try_timedelta(v)
    elif inferred_type == "nat":

        # if all NaT, return as datetime
        if isna(v).all():
            # error: Incompatible types in assignment (expression has type
            # "ExtensionArray", variable has type "Union[ndarray, List[Any]]")
            value = try_datetime(v)  # type: ignore[assignment]
        else:

            # We have at least a NaT and a string
            # try timedelta first to avoid spurious datetime conversions
            # e.g. '00:00:01' is a timedelta but technically is also a datetime
            value = try_timedelta(v)
            if lib.infer_dtype(value, skipna=False) in ["mixed"]:
                # cannot skip missing values, as NaT implies that the string
                # is actually a datetime

                # error: Incompatible types in assignment (expression has type
                # "ExtensionArray", variable has type "Union[ndarray, List[Any]]")
                value = try_datetime(v)  # type: ignore[assignment]

    if value.dtype.kind in ["m", "M"] and seen_str:
        warnings.warn(
            f"Inferring {value.dtype} from data containing strings is deprecated "
            "and will be removed in a future version. To retain the old behavior "
            "explicitly pass Series(data, dtype={value.dtype})",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
    return value
