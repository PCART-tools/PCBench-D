def maybe_promote(dtype, fill_value=np.nan):
    """
    Find the minimal dtype that can hold both the given dtype and fill_value.

    Parameters
    ----------
    dtype : np.dtype or ExtensionDtype
    fill_value : scalar, default np.nan

    Returns
    -------
    dtype
        Upcasted from dtype argument if necessary.
    fill_value
        Upcasted from fill_value argument if necessary.
    """
    if not is_scalar(fill_value) and not is_object_dtype(dtype):
        # with object dtype there is nothing to promote, and the user can
        #  pass pretty much any weird fill_value they like
        raise ValueError("fill_value must be a scalar")

    # if we passed an array here, determine the fill value by dtype
    if isinstance(fill_value, np.ndarray):
        if issubclass(fill_value.dtype.type, (np.datetime64, np.timedelta64)):
            fill_value = fill_value.dtype.type("NaT", "ns")
        else:

            # we need to change to object type as our
            # fill_value is of object type
            if fill_value.dtype == np.object_:
                dtype = np.dtype(np.object_)
            fill_value = np.nan

        if dtype == np.object_ or dtype.kind in ["U", "S"]:
            # We treat string-like dtypes as object, and _always_ fill
            #  with np.nan
            fill_value = np.nan
            dtype = np.dtype(np.object_)

    # returns tuple of (dtype, fill_value)
    if issubclass(dtype.type, np.datetime64):
        if isinstance(fill_value, datetime) and fill_value.tzinfo is not None:
            # Trying to insert tzaware into tznaive, have to cast to object
            dtype = np.dtype(np.object_)
        elif is_integer(fill_value) or (is_float(fill_value) and not isna(fill_value)):
            dtype = np.dtype(np.object_)
        else:
            try:
                fill_value = tslibs.Timestamp(fill_value).to_datetime64()
            except (TypeError, ValueError):
                dtype = np.dtype(np.object_)
    elif issubclass(dtype.type, np.timedelta64):
        if (
            is_integer(fill_value)
            or (is_float(fill_value) and not np.isnan(fill_value))
            or isinstance(fill_value, str)
        ):
            # TODO: What about str that can be a timedelta?
            dtype = np.dtype(np.object_)
        else:
            try:
                fv = tslibs.Timedelta(fill_value)
            except ValueError:
                dtype = np.dtype(np.object_)
            else:
                if fv is NaT:
                    # NaT has no `to_timedelta64` method
                    fill_value = np.timedelta64("NaT", "ns")
                else:
                    fill_value = fv.to_timedelta64()
    elif is_datetime64tz_dtype(dtype):
        if isna(fill_value):
            fill_value = NaT
        elif not isinstance(fill_value, datetime):
            dtype = np.dtype(np.object_)
        elif fill_value.tzinfo is None:
            dtype = np.dtype(np.object_)
        elif not tz_compare(fill_value.tzinfo, dtype.tz):
            # TODO: sure we want to cast here?
            dtype = np.dtype(np.object_)

    elif is_extension_array_dtype(dtype) and isna(fill_value):
        fill_value = dtype.na_value

    elif is_float(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, np.integer):
            dtype = np.dtype(np.float64)

        elif dtype.kind == "f":
            mst = np.min_scalar_type(fill_value)
            if mst > dtype:
                # e.g. mst is np.float64 and dtype is np.float32
                dtype = mst

        elif dtype.kind == "c":
            mst = np.min_scalar_type(fill_value)
            dtype = np.promote_types(dtype, mst)

    elif is_bool(fill_value):
        if not issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

    elif is_integer(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, np.integer):
            if not np.can_cast(fill_value, dtype):
                # upcast to prevent overflow
                mst = np.min_scalar_type(fill_value)
                dtype = np.promote_types(dtype, mst)
                if dtype.kind == "f":
                    # Case where we disagree with numpy
                    dtype = np.dtype(np.object_)

    elif is_complex(fill_value):
        if issubclass(dtype.type, np.bool_):
            dtype = np.dtype(np.object_)

        elif issubclass(dtype.type, (np.integer, np.floating)):
            mst = np.min_scalar_type(fill_value)
            dtype = np.promote_types(dtype, mst)

        elif dtype.kind == "c":
            mst = np.min_scalar_type(fill_value)
            if mst > dtype:
                # e.g. mst is np.complex128 and dtype is np.complex64
                dtype = mst

    elif fill_value is None:
        if is_float_dtype(dtype) or is_complex_dtype(dtype):
            fill_value = np.nan
        elif is_integer_dtype(dtype):
            dtype = np.float64
            fill_value = np.nan
        elif is_datetime_or_timedelta_dtype(dtype):
            fill_value = dtype.type("NaT", "ns")
        else:
            dtype = np.dtype(np.object_)
            fill_value = np.nan
    else:
        dtype = np.dtype(np.object_)

    # in case we have a string that looked like a number
    if is_extension_array_dtype(dtype):
        pass
    elif issubclass(np.dtype(dtype).type, (bytes, str)):
        dtype = np.dtype(np.object_)

    fill_value = _ensure_dtype_type(fill_value, dtype)
    return dtype, fill_value
