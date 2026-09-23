def i8_boxer(arr_or_dtype):
    """ return the scalar boxer for the dtype """
    if is_datetime64_dtype(arr_or_dtype):
        return lib.Timestamp
    elif is_timedelta64_dtype(arr_or_dtype):
        return lambda x: lib.Timedelta(x,unit='ns')
    raise ValueError("cannot find a scalar boxer for {0}".format(arr_or_dtype))
