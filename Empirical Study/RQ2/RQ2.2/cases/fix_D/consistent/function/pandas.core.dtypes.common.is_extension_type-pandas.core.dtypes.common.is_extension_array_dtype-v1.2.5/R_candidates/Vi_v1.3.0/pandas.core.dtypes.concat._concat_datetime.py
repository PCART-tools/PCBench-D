def _concat_datetime(to_concat, axis=0):
    """
    provide concatenation of an datetimelike array of arrays each of which is a
    single M8[ns], datetime64[ns, tz] or m8[ns] dtype

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation

    Returns
    -------
    a single array, preserving the combined dtypes
    """
    to_concat = [ensure_wrapped_if_datetimelike(x) for x in to_concat]

    single_dtype = len({x.dtype for x in to_concat}) == 1

    # multiple types, need to coerce to object
    if not single_dtype:
        # ensure_wrapped_if_datetimelike ensures that astype(object) wraps
        #  in Timestamp/Timedelta
        return _concatenate_2d([x.astype(object) for x in to_concat], axis=axis)

    result = type(to_concat[0])._concat_same_type(to_concat, axis=axis)
    return result
