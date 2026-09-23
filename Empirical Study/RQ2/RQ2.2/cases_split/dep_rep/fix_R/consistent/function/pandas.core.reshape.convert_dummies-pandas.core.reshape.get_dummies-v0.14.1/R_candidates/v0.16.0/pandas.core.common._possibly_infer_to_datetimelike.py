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
    value : np.array
    convert_dates : boolean, default False
       if True try really hard to convert dates (such as datetime.date), other
       leave inferred dtype 'date' alone

    """

    v = value
    if not is_list_like(v):
        v = [v]
    v = np.array(v,copy=False)
    shape = v.shape
    if not v.ndim == 1:
        v = v.ravel()

    if len(v):

        def _try_datetime(v):
            # safe coerce to datetime64
            try:
                return tslib.array_to_datetime(v, raise_=True).reshape(shape)
            except:
                return v

        def _try_timedelta(v):
            # safe coerce to timedelta64

            # will try first with a string & object conversion
            from pandas.tseries.timedeltas import to_timedelta
            try:
                return to_timedelta(v).values.reshape(shape)
            except:
                return v

        # do a quick inference for perf
        sample = v[:min(3,len(v))]
        inferred_type = lib.infer_dtype(sample)

        if inferred_type in ['datetime', 'datetime64'] or (convert_dates and inferred_type in ['date']):
            value = _try_datetime(v).reshape(shape)
        elif inferred_type in ['timedelta', 'timedelta64']:
            value = _try_timedelta(v).reshape(shape)

        # its possible to have nulls intermixed within the datetime or timedelta
        # these will in general have an inferred_type of 'mixed', so have to try
        # both datetime and timedelta

        # try timedelta first to avoid spurious datetime conversions
        # e.g. '00:00:01' is a timedelta but technically is also a datetime
        elif inferred_type in ['mixed']:

            if lib.is_possible_datetimelike_array(_ensure_object(v)):
                value = _try_timedelta(v).reshape(shape)
                if lib.infer_dtype(value) in ['mixed']:
                    value = _try_datetime(v).reshape(shape)

    return value
