def _astype_nansafe(arr, dtype, copy=True):
    """ return a view if copy is False, but
        need to be very careful as the result shape could change! """
    if not isinstance(dtype, np.dtype):
        dtype = _coerce_to_dtype(dtype)

    if issubclass(dtype.type, compat.text_type):
        # in Py3 that's str, in Py2 that's unicode
        return lib.astype_unicode(arr.ravel()).reshape(arr.shape)
    elif issubclass(dtype.type, compat.string_types):
        return lib.astype_str(arr.ravel()).reshape(arr.shape)
    elif is_datetime64_dtype(arr):
        if dtype == object:
            return tslib.ints_to_pydatetime(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)
        elif dtype != _NS_DTYPE:
            raise TypeError("cannot astype a datetimelike from [%s] to [%s]" %
                            (arr.dtype, dtype))
        return arr.astype(_NS_DTYPE)
    elif is_timedelta64_dtype(arr):
        if dtype == np.int64:
            return arr.view(dtype)
        elif dtype == object:
            return tslib.ints_to_pytimedelta(arr.view(np.int64))

        # in py3, timedelta64[ns] are int64
        elif ((compat.PY3 and dtype not in [_INT64_DTYPE, _TD_DTYPE]) or
              (not compat.PY3 and dtype != _TD_DTYPE)):

            # allow frequency conversions
            if dtype.kind == 'm':
                mask = isnull(arr)
                result = arr.astype(dtype).astype(np.float64)
                result[mask] = np.nan
                return result

            raise TypeError("cannot astype a timedelta from [%s] to [%s]" %
                            (arr.dtype, dtype))

        return arr.astype(_TD_DTYPE)
    elif (np.issubdtype(arr.dtype, np.floating) and
          np.issubdtype(dtype, np.integer)):

        if np.isnan(arr).any():
            raise ValueError('Cannot convert NA to integer')
    elif arr.dtype == np.object_ and np.issubdtype(dtype.type, np.integer):
        # work around NumPy brokenness, #1987
        return lib.astype_intsafe(arr.ravel(), dtype).reshape(arr.shape)

    if copy:
        return arr.astype(dtype)
    return arr.view(dtype)
