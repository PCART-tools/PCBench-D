def infer_dtype_from_scalar(val, pandas_dtype: bool = False) -> tuple[DtypeObj, Any]:
    """
    Interpret the dtype from a scalar.

    Parameters
    ----------
    pandas_dtype : bool, default False
        whether to infer dtype including pandas extension types.
        If False, scalar belongs to pandas extension types is inferred as
        object
    """
    dtype: DtypeObj = np.dtype(object)

    # a 1-element ndarray
    if isinstance(val, np.ndarray):
        if val.ndim != 0:
            msg = "invalid ndarray passed to infer_dtype_from_scalar"
            raise ValueError(msg)

        dtype = val.dtype
        val = lib.item_from_zerodim(val)

    elif isinstance(val, str):

        # If we create an empty array using a string to infer
        # the dtype, NumPy will only allocate one character per entry
        # so this is kind of bad. Alternately we could use np.repeat
        # instead of np.empty (but then you still don't want things
        # coming out as np.str_!

        dtype = np.dtype(object)

    elif isinstance(val, (np.datetime64, datetime)):
        try:
            val = Timestamp(val)
        except OutOfBoundsDatetime:
            return np.dtype(object), val

        # error: Non-overlapping identity check (left operand type: "Timestamp",
        # right operand type: "NaTType")
        if val is NaT or val.tz is None:  # type: ignore[comparison-overlap]
            dtype = np.dtype("M8[ns]")
            val = val.to_datetime64()
        else:
            if pandas_dtype:
                dtype = DatetimeTZDtype(unit="ns", tz=val.tz)
            else:
                # return datetimetz as object
                return np.dtype(object), val

    elif isinstance(val, (np.timedelta64, timedelta)):
        try:
            val = Timedelta(val)
        except (OutOfBoundsTimedelta, OverflowError):
            dtype = np.dtype(object)
        else:
            dtype = np.dtype("m8[ns]")
            val = np.timedelta64(val.value, "ns")

    elif is_bool(val):
        dtype = np.dtype(np.bool_)

    elif is_integer(val):
        if isinstance(val, np.integer):
            dtype = np.dtype(type(val))
        else:
            dtype = np.dtype(np.int64)

        try:
            np.array(val, dtype=dtype)
        except OverflowError:
            dtype = np.array(val).dtype

    elif is_float(val):
        if isinstance(val, np.floating):
            dtype = np.dtype(type(val))
        else:
            dtype = np.dtype(np.float64)

    elif is_complex(val):
        dtype = np.dtype(np.complex_)

    elif pandas_dtype:
        if lib.is_period(val):
            dtype = PeriodDtype(freq=val.freq)
        elif lib.is_interval(val):
            subtype = infer_dtype_from_scalar(val.left, pandas_dtype=True)[0]
            dtype = IntervalDtype(subtype=subtype, closed=val.closed)

    return dtype, val
