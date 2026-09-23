def _possibly_infer_to_datetimelike(value, convert_dates=False):
    """
    we might have a array (or single object) that is datetime like,
    and no dtype is passed don't change the value unless we find a
    datetime/timedelta set

    this is pretty strict in that a datetime/timedelta is REQUIRED
    in addition to possible nulls/string likes

    ONLY strings are NOT datetimelike

    Parameters
    ----------
    value : np.array / Series / Index / list-like
    convert_dates : boolean, default False
       if True try really hard to convert dates (such as datetime.date), other
       leave inferred dtype 'date' alone

    """

    if isinstance(value, (gt.ABCDatetimeIndex, gt.ABCPeriodIndex)):
        return value
    elif isinstance(value, gt.ABCSeries):
        if isinstance(value._values, gt.ABCDatetimeIndex):
            return value._values

    v = value
    if not is_list_like(v):
        v = [v]
    v = np.array(v, copy=False)
    shape = v.shape
    if not v.ndim == 1:
        v = v.ravel()

    if len(v):

        def _try_datetime(v):
            # safe coerce to datetime64
            try:
                v = tslib.array_to_datetime(v, errors='raise')
            except ValueError:

                # we might have a sequence of the same-datetimes with tz's
                # if so coerce to a DatetimeIndex; if they are not the same,
                # then these stay as object dtype
                try:
                    from pandas import to_datetime
                    return to_datetime(v)
                except:
                    pass

            except:
                pass

            return v.reshape(shape)

        def _try_timedelta(v):
            # safe coerce to timedelta64

            # will try first with a string & object conversion
            from pandas.tseries.timedeltas import to_timedelta
            try:
                return to_timedelta(v)._values.reshape(shape)
            except:
                return v

        # do a quick inference for perf
        sample = v[:min(3, len(v))]
        inferred_type = lib.infer_dtype(sample)

        if (inferred_type in ['datetime', 'datetime64'] or
                (convert_dates and inferred_type in ['date'])):
            value = _try_datetime(v)
        elif inferred_type in ['timedelta', 'timedelta64']:
            value = _try_timedelta(v)

        # It's possible to have nulls intermixed within the datetime or
        # timedelta.  These will in general have an inferred_type of 'mixed',
        # so have to try both datetime and timedelta.

        # try timedelta first to avoid spurious datetime conversions
        # e.g. '00:00:01' is a timedelta but technically is also a datetime
        elif inferred_type in ['mixed']:

            if lib.is_possible_datetimelike_array(_ensure_object(v)):
                value = _try_timedelta(v)
                if lib.infer_dtype(value) in ['mixed']:
                    value = _try_datetime(v)

    return value
