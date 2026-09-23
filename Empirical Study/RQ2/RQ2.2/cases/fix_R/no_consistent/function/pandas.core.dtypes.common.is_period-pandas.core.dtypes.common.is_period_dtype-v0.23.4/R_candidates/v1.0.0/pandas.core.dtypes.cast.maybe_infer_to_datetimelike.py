def maybe_infer_to_datetimelike(value, convert_dates: bool = False):
    """
    we might have a array (or single object) that is datetime like,
    and no dtype is passed don't change the value unless we find a
    datetime/timedelta set

    this is pretty strict in that a datetime/timedelta is REQUIRED
    in addition to possible nulls/string likes

    Parameters
    ----------
    value : np.array / Series / Index / list-like
    convert_dates : bool, default False
       if True try really hard to convert dates (such as datetime.date), other
       leave inferred dtype 'date' alone

    """

    # TODO: why not timedelta?
    if isinstance(
        value, (ABCDatetimeIndex, ABCPeriodIndex, ABCDatetimeArray, ABCPeriodArray)
    ):
        return value
    elif isinstance(value, ABCSeries):
        if isinstance(value._values, ABCDatetimeIndex):
            return value._values

    v = value

    if not is_list_like(v):
        v = [v]
    v = np.array(v, copy=False)

    # we only care about object dtypes
    if not is_object_dtype(v):
        return value

    shape = v.shape
    if not v.ndim == 1:
        v = v.ravel()

    if not len(v):
        return value

    def try_datetime(v):
        # safe coerce to datetime64
        try:
            # GH19671
            v = tslib.array_to_datetime(v, require_iso8601=True, errors="raise")[0]
        except ValueError:

            # we might have a sequence of the same-datetimes with tz's
            # if so coerce to a DatetimeIndex; if they are not the same,
            # then these stay as object dtype, xref GH19671
            from pandas._libs.tslibs import conversion
            from pandas import DatetimeIndex

            try:

                values, tz = conversion.datetime_to_datetime64(v)
                return DatetimeIndex(values).tz_localize("UTC").tz_convert(tz=tz)
            except (ValueError, TypeError):
                pass

        except Exception:
            pass

        return v.reshape(shape)

    def try_timedelta(v):
        # safe coerce to timedelta64

        # will try first with a string & object conversion
        from pandas import to_timedelta

        try:
            return to_timedelta(v)._ndarray_values.reshape(shape)
        except ValueError:
            return v.reshape(shape)

    inferred_type = lib.infer_datetimelike_array(ensure_object(v))

    if inferred_type == "date" and convert_dates:
        value = try_datetime(v)
    elif inferred_type == "datetime":
        value = try_datetime(v)
    elif inferred_type == "timedelta":
        value = try_timedelta(v)
    elif inferred_type == "nat":

        # if all NaT, return as datetime
        if isna(v).all():
            value = try_datetime(v)
        else:

            # We have at least a NaT and a string
            # try timedelta first to avoid spurious datetime conversions
            # e.g. '00:00:01' is a timedelta but technically is also a datetime
            value = try_timedelta(v)
            if lib.infer_dtype(value, skipna=False) in ["mixed"]:
                # cannot skip missing values, as NaT implies that the string
                # is actually a datetime
                value = try_datetime(v)

    return value
