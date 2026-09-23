    def __init__(
        self, values, dtype=TD64NS_DTYPE, freq=lib.no_default, copy: bool = False
    ):
        values = extract_array(values, extract_numpy=True)
        if isinstance(values, IntegerArray):
            values = values.to_numpy("int64", na_value=tslibs.iNaT)

        inferred_freq = getattr(values, "_freq", None)
        explicit_none = freq is None
        freq = freq if freq is not lib.no_default else None

        if isinstance(values, type(self)):
            if explicit_none:
                # dont inherit from values
                pass
            elif freq is None:
                freq = values.freq
            elif freq and values.freq:
                freq = to_offset(freq)
                freq, _ = dtl.validate_inferred_freq(freq, values.freq, False)
            values = values._ndarray

        if not isinstance(values, np.ndarray):
            msg = (
                f"Unexpected type '{type(values).__name__}'. 'values' must be a "
                "TimedeltaArray, ndarray, or Series or Index containing one of those."
            )
            raise ValueError(msg)
        if values.ndim not in [1, 2]:
            raise ValueError("Only 1-dimensional input arrays are supported.")

        if values.dtype == "i8":
            # for compat with datetime/timedelta/period shared methods,
            #  we can sometimes get here with int64 values.  These represent
            #  nanosecond UTC (or tz-naive) unix timestamps
            values = values.view(TD64NS_DTYPE)

        _validate_td64_dtype(values.dtype)
        dtype = _validate_td64_dtype(dtype)

        if freq == "infer":
            msg = (
                "Frequency inference not allowed in TimedeltaArray.__init__. "
                "Use 'pd.array()' instead."
            )
            raise ValueError(msg)

        if copy:
            values = values.copy()
        if freq:
            freq = to_offset(freq)

        NDArrayBacked.__init__(self, values=values, dtype=dtype)
        self._freq = freq

        if inferred_freq is None and freq is not None:
            type(self)._validate_frequency(self, freq)
