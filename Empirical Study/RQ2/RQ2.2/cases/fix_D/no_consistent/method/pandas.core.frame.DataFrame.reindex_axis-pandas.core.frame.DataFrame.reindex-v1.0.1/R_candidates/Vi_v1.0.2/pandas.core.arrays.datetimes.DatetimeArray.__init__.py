    def __init__(self, values, dtype=_NS_DTYPE, freq=None, copy=False):
        if isinstance(values, (ABCSeries, ABCIndexClass)):
            values = values._values

        inferred_freq = getattr(values, "_freq", None)

        if isinstance(values, type(self)):
            # validation
            dtz = getattr(dtype, "tz", None)
            if dtz and values.tz is None:
                dtype = DatetimeTZDtype(tz=dtype.tz)
            elif dtz and values.tz:
                if not timezones.tz_compare(dtz, values.tz):
                    msg = (
                        "Timezone of the array and 'dtype' do not match. "
                        f"'{dtz}' != '{values.tz}'"
                    )
                    raise TypeError(msg)
            elif values.tz:
                dtype = values.dtype

            if freq is None:
                freq = values.freq
            values = values._data

        if not isinstance(values, np.ndarray):
            msg = (
                f"Unexpected type '{type(values).__name__}'. 'values' must be "
                "a DatetimeArray ndarray, or Series or Index containing one of those."
            )
            raise ValueError(msg)
        if values.ndim not in [1, 2]:
            raise ValueError("Only 1-dimensional input arrays are supported.")

        if values.dtype == "i8":
            # for compat with datetime/timedelta/period shared methods,
            #  we can sometimes get here with int64 values.  These represent
            #  nanosecond UTC (or tz-naive) unix timestamps
            values = values.view(_NS_DTYPE)

        if values.dtype != _NS_DTYPE:
            msg = (
                "The dtype of 'values' is incorrect. Must be 'datetime64[ns]'."
                f" Got {values.dtype} instead."
            )
            raise ValueError(msg)

        dtype = _validate_dt64_dtype(dtype)

        if freq == "infer":
            msg = (
                "Frequency inference not allowed in DatetimeArray.__init__. "
                "Use 'pd.array()' instead."
            )
            raise ValueError(msg)

        if copy:
            values = values.copy()
        if freq:
            freq = to_offset(freq)
        if getattr(dtype, "tz", None):
            # https://github.com/pandas-dev/pandas/issues/18595
            # Ensure that we have a standard timezone for pytz objects.
            # Without this, things like adding an array of timedeltas and
            # a  tz-aware Timestamp (with a tz specific to its datetime) will
            # be incorrect(ish?) for the array as a whole
            dtype = DatetimeTZDtype(tz=timezones.tz_standardize(dtype.tz))

        self._data = values
        self._dtype = dtype
        self._freq = freq

        if inferred_freq is None and freq is not None:
            type(self)._validate_frequency(self, freq)
