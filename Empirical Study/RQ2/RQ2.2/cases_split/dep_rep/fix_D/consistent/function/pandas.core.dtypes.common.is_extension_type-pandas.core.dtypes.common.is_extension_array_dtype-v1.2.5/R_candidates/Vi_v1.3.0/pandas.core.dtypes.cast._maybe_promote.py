def _maybe_promote(dtype: np.dtype, fill_value=np.nan):
    # The actual implementation of the function, use `maybe_promote` above for
    # a cached version.
    if not is_scalar(fill_value):
        # with object dtype there is nothing to promote, and the user can
        #  pass pretty much any weird fill_value they like
        if not is_object_dtype(dtype):
            # with object dtype there is nothing to promote, and the user can
            #  pass pretty much any weird fill_value they like
            raise ValueError("fill_value must be a scalar")
        dtype = np.dtype(object)
        return dtype, fill_value

    kinds = ["i", "u", "f", "c", "m", "M"]
    if is_valid_na_for_dtype(fill_value, dtype) and dtype.kind in kinds:
        dtype = ensure_dtype_can_hold_na(dtype)
        fv = na_value_for_dtype(dtype)
        return dtype, fv

    elif isna(fill_value):
        dtype = np.dtype(object)
        if fill_value is None:
            # but we retain e.g. pd.NA
            fill_value = np.nan
        return dtype, fill_value

    # returns tuple of (dtype, fill_value)
    if issubclass(dtype.type, np.datetime64):
        inferred, fv = infer_dtype_from_scalar(fill_value, pandas_dtype=True)
        if inferred == dtype:
            return dtype, fv

        # TODO(2.0): once this deprecation is enforced, this whole case
        # becomes equivalent to:
        #  dta = DatetimeArray._from_sequence([], dtype="M8[ns]")
        #  try:
        #      fv = dta._validate_setitem_value(fill_value)
        #      return dta.dtype, fv
        #  except (ValueError, TypeError):
        #      return np.dtype(object), fill_value
        if isinstance(fill_value, date) and not isinstance(fill_value, datetime):
            # deprecate casting of date object to match infer_dtype_from_scalar
            #  and DatetimeArray._validate_setitem_value
            try:
                fv = Timestamp(fill_value).to_datetime64()
            except OutOfBoundsDatetime:
                pass
            else:
                warnings.warn(
                    "Using a `date` object for fill_value with `datetime64[ns]` "
                    "dtype is deprecated. In a future version, this will be cast "
                    "to object dtype. Pass `fill_value=Timestamp(date_obj)` instead.",
                    FutureWarning,
                    stacklevel=8,
                )
                return dtype, fv
        elif isinstance(fill_value, str):
            try:
                # explicitly wrap in str to convert np.str_
                fv = Timestamp(str(fill_value))
            except (ValueError, TypeError):
                pass
            else:
                if fv.tz is None:
                    return dtype, fv.asm8

        return np.dtype("object"), fill_value

    elif issubclass(dtype.type, np.timedelta64):
        inferred, fv = infer_dtype_from_scalar(fill_value, pandas_dtype=True)
        if inferred == dtype:
            return dtype, fv

        return np.dtype("object"), fill_value

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

    else:
        dtype = np.dtype(np.object_)

    # in case we have a string that looked like a number
    if issubclass(dtype.type, (bytes, str)):
        dtype = np.dtype(np.object_)

    fill_value = _ensure_dtype_type(fill_value, dtype)
    return dtype, fill_value
