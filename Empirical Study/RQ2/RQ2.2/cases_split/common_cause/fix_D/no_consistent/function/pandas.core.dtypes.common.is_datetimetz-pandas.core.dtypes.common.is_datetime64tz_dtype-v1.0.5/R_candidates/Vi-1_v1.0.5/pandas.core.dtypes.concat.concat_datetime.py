def concat_datetime(to_concat, axis=0, typs=None):
    """
    provide concatenation of an datetimelike array of arrays each of which is a
    single M8[ns], datetimet64[ns, tz] or m8[ns] dtype

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation
    typs : set of to_concat dtypes

    Returns
    -------
    a single array, preserving the combined dtypes
    """

    if typs is None:
        typs = get_dtype_kinds(to_concat)

    # multiple types, need to coerce to object
    if len(typs) != 1:
        return _concatenate_2d(
            [_convert_datetimelike_to_object(x) for x in to_concat], axis=axis
        )

    # must be single dtype
    if any(typ.startswith("datetime") for typ in typs):

        if "datetime" in typs:
            to_concat = [x.astype(np.int64, copy=False) for x in to_concat]
            return _concatenate_2d(to_concat, axis=axis).view(_NS_DTYPE)
        else:
            # when to_concat has different tz, len(typs) > 1.
            # thus no need to care
            return _concat_datetimetz(to_concat)

    elif "timedelta" in typs:
        return _concatenate_2d([x.view(np.int64) for x in to_concat], axis=axis).view(
            _TD_DTYPE
        )

    elif any(typ.startswith("period") for typ in typs):
        assert len(typs) == 1
        cls = to_concat[0]
        new_values = cls._concat_same_type(to_concat)
        return new_values
