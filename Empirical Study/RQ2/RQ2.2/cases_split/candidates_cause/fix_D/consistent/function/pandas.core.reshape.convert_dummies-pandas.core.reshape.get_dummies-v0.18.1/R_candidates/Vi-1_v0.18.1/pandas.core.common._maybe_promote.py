def _maybe_promote(dtype, fill_value=np.nan):

    # if we passed an array here, determine the fill value by dtype
    if isinstance(fill_value, np.ndarray):
        if issubclass(fill_value.dtype.type, (np.datetime64, np.timedelta64)):
            fill_value = tslib.iNaT
        else:

            # we need to change to object type as our
            # fill_value is of object type
            if fill_value.dtype == np.object_:
                dtype = np.dtype(np.object_)
            fill_value = np.nan

    # returns tuple of (dtype, fill_value)
    if issubclass(dtype.type, (np.datetime64, np.timedelta64)):
        # for now: refuse to upcast datetime64
        # (this is because datetime64 will not implicitly upconvert
        #  to object correctly as of numpy 1.6.1)
        if isnull(fill_value):
            fill_value = tslib.iNaT
        else:
            if issubclass(dtype.type, np.datetime64):
                try:
                    fill_value = lib.Timestamp(fill_value).value
                except:
                    # the proper thing to do here would probably be to upcast
                    # to object (but numpy 1.6.1 doesn't do this properly)
                    fill_value = tslib.iNaT
            elif issubclass(dtype.type, np.timedelta64):
                try:
                    fill_value = lib.Timedelta(fill_value).value
                except:
                    # as for datetimes, cannot upcast to object
                    fill_value = tslib.iNaT
            else:
                fill_value = tslib.iNaT
    elif is_datetimetz(dtype):
        if isnull(fill_value):
            fill_value = tslib.iNaT
    elif is_float(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.object_
        elif issubclass(dtype.type, np.integer):
            dtype = np.float64
    elif is_bool(fill_value):
        if not issubclass(dtype.type, np.bool_):
            dtype = np.object_
    elif is_integer(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.object_
        elif issubclass(dtype.type, np.integer):
            # upcast to prevent overflow
            arr = np.asarray(fill_value)
            if arr != arr.astype(dtype):
                dtype = arr.dtype
    elif is_complex(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.object_
        elif issubclass(dtype.type, (np.integer, np.floating)):
            dtype = np.complex128
    elif fill_value is None:
        if is_float_dtype(dtype) or is_complex_dtype(dtype):
            fill_value = np.nan
        elif is_integer_dtype(dtype):
            dtype = np.float64
            fill_value = np.nan
        elif is_datetime_or_timedelta_dtype(dtype):
            fill_value = tslib.iNaT
        else:
            dtype = np.object_
    else:
        dtype = np.object_

    # in case we have a string that looked like a number
    if is_categorical_dtype(dtype):
        pass
    elif is_datetimetz(dtype):
        pass
    elif issubclass(np.dtype(dtype).type, compat.string_types):
        dtype = np.object_

    return dtype, fill_value
