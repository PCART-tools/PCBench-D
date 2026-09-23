def _convert_datetimelike_to_object(x):
    # coerce datetimelike array to object dtype

    # if dtype is of datetimetz or timezone
    if x.dtype.kind == _NS_DTYPE.kind:
        if getattr(x, "tz", None) is not None:
            x = np.asarray(x.astype(object))
        else:
            shape = x.shape
            x = tslib.ints_to_pydatetime(x.view(np.int64).ravel(), box="timestamp")
            x = x.reshape(shape)

    elif x.dtype == _TD_DTYPE:
        shape = x.shape
        x = tslibs.ints_to_pytimedelta(x.view(np.int64).ravel(), box=True)
        x = x.reshape(shape)

    return x
