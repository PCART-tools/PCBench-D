def _infer_dtype_from_scalar(val):
    """ interpret the dtype from a scalar, upcast floats and ints
        return the new value and the dtype """

    dtype = np.object_

    # a 1-element ndarray
    if isinstance(val, np.ndarray):
        if val.ndim != 0:
            raise ValueError(
                "invalid ndarray passed to _infer_dtype_from_scalar")

        dtype = val.dtype
        val = val.item()

    elif isinstance(val, compat.string_types):

        # If we create an empty array using a string to infer
        # the dtype, NumPy will only allocate one character per entry
        # so this is kind of bad. Alternately we could use np.repeat
        # instead of np.empty (but then you still don't want things
        # coming out as np.str_!

        dtype = np.object_

    elif isinstance(val, (np.datetime64, datetime)) and getattr(val,'tz',None) is None:
        val = lib.Timestamp(val).value
        dtype = np.dtype('M8[ns]')

    elif isinstance(val, (np.timedelta64, timedelta)):
        val = tslib.convert_to_timedelta(val,'ns')
        dtype = np.dtype('m8[ns]')

    elif is_bool(val):
        dtype = np.bool_

    # provide implicity upcast on scalars
    elif is_integer(val):
        dtype = np.int64

    elif is_float(val):
        dtype = np.float64

    elif is_complex(val):
        dtype = np.complex_

    return dtype, val
