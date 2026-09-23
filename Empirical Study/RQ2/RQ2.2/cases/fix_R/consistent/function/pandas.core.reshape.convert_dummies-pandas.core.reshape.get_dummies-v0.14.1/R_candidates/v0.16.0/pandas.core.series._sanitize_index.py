def _sanitize_index(data, index, copy=False):
    """ sanitize an index type to return an ndarray of the underlying, pass thru a non-Index """

    if len(data) != len(index):
        raise ValueError('Length of values does not match length of '
                         'index')

    if isinstance(data, PeriodIndex):
        data = data.asobject
    elif isinstance(data, DatetimeIndex):
        data = data._to_embed(keep_tz=True)
        if copy:
            data = data.copy()
    elif isinstance(data, np.ndarray):

        # coerce datetimelike types
        if data.dtype.kind in ['M','m']:
            data = _sanitize_array(data, index, copy=copy)

    return data
