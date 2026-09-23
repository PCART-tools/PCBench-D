def _possibly_cast_to_datetime(value, dtype, errors='raise'):
    """ try to cast the array/value to a datetimelike dtype, converting float
    nan to iNaT
    """
    from pandas.tseries.timedeltas import to_timedelta
    from pandas.tseries.tools import to_datetime

    if dtype is not None:
        if isinstance(dtype, compat.string_types):
            dtype = np.dtype(dtype)

        is_datetime64 = is_datetime64_dtype(dtype)
        is_datetime64tz = is_datetime64tz_dtype(dtype)
        is_timedelta64 = is_timedelta64_dtype(dtype)

        if is_datetime64 or is_datetime64tz or is_timedelta64:

            # force the dtype if needed
            if is_datetime64 and not is_dtype_equal(dtype, _NS_DTYPE):
                if dtype.name == 'datetime64[ns]':
                    dtype = _NS_DTYPE
                else:
                    raise TypeError("cannot convert datetimelike to "
                                    "dtype [%s]" % dtype)
            elif is_datetime64tz:

                # our NaT doesn't support tz's
                # this will coerce to DatetimeIndex with
                # a matching dtype below
                if lib.isscalar(value) and isnull(value):
                    value = [value]

            elif is_timedelta64 and not is_dtype_equal(dtype, _TD_DTYPE):
                if dtype.name == 'timedelta64[ns]':
                    dtype = _TD_DTYPE
                else:
                    raise TypeError("cannot convert timedeltalike to "
                                    "dtype [%s]" % dtype)

            if lib.isscalar(value):
                if value == tslib.iNaT or isnull(value):
                    value = tslib.iNaT
            else:
                value = np.array(value, copy=False)

                # have a scalar array-like (e.g. NaT)
                if value.ndim == 0:
                    value = tslib.iNaT

                # we have an array of datetime or timedeltas & nulls
                elif np.prod(value.shape) or not is_dtype_equal(value.dtype,
                                                                dtype):
                    try:
                        if is_datetime64:
                            value = to_datetime(value, errors=errors)._values
                        elif is_datetime64tz:
                            # input has to be UTC at this point, so just
                            # localize
                            value = to_datetime(
                                value,
                                errors=errors).tz_localize(dtype.tz)
                        elif is_timedelta64:
                            value = to_timedelta(value, errors=errors)._values
                    except (AttributeError, ValueError, TypeError):
                        pass

        # coerce datetimelike to object
        elif is_datetime64_dtype(value) and not is_datetime64_dtype(dtype):
            if is_object_dtype(dtype):
                ints = np.asarray(value).view('i8')
                return tslib.ints_to_pydatetime(ints)

            # we have a non-castable dtype that was passed
            raise TypeError('Cannot cast datetime64 to %s' % dtype)

    else:

        is_array = isinstance(value, np.ndarray)

        # catch a datetime/timedelta that is not of ns variety
        # and no coercion specified
        if is_array and value.dtype.kind in ['M', 'm']:
            dtype = value.dtype

            if dtype.kind == 'M' and dtype != _NS_DTYPE:
                value = value.astype(_NS_DTYPE)

            elif dtype.kind == 'm' and dtype != _TD_DTYPE:
                value = to_timedelta(value)

        # only do this if we have an array and the dtype of the array is not
        # setup already we are not an integer/object, so don't bother with this
        # conversion
        elif not (is_array and not (issubclass(value.dtype.type, np.integer) or
                                    value.dtype == np.object_)):
            value = _possibly_infer_to_datetimelike(value)

    return value
