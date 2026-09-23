    def __init__(self, values, dtype=_TD_DTYPE, freq=None, copy=False):
        if isinstance(values, (ABCSeries, ABCIndexClass)):
            values = values._values

        inferred_freq = getattr(values, "_freq", None)

        if isinstance(values, type(self)):
            if freq is None:
                freq = values.freq
            elif freq and values.freq:
                freq = to_offset(freq)
                freq, _ = dtl.validate_inferred_freq(freq, values.freq, False)
            values = values._data

        if not isinstance(values, np.ndarray):
            msg = (
                f"Unexpected type '{type(values).__name__}'. 'values' must be a "
                "TimedeltaArray ndarray, or Series or Index containing one of those."
            )
            raise ValueError(msg)
        if values.ndim not in [1, 2]:
            raise ValueError("Only 1-dimensional input arrays are supported.")

        if values.dtype == "i8":
            # for compat with datetime/timedelta/period shared methods,
            #  we can sometimes get here with int64 values.  These represent
            #  nanosecond UTC (or tz-naive) unix timestamps
            values = values.view(_TD_DTYPE)

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

        self._data = values
        self._dtype = dtype
        self._freq = freq

        if inferred_freq is None and freq is not None:
            type(self)._validate_frequency(self, freq)
