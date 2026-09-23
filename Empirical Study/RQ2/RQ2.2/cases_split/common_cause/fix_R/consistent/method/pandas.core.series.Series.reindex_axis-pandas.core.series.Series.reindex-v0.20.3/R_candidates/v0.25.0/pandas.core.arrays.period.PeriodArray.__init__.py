    def __init__(self, values, freq=None, dtype=None, copy=False):
        freq = validate_dtype_freq(dtype, freq)

        if freq is not None:
            freq = Period._maybe_convert_freq(freq)

        if isinstance(values, ABCSeries):
            values = values._values
            if not isinstance(values, type(self)):
                raise TypeError("Incorrect dtype")

        elif isinstance(values, ABCPeriodIndex):
            values = values._values

        if isinstance(values, type(self)):
            if freq is not None and freq != values.freq:
                msg = DIFFERENT_FREQ.format(
                    cls=type(self).__name__,
                    own_freq=values.freq.freqstr,
                    other_freq=freq.freqstr,
                )
                raise IncompatibleFrequency(msg)
            values, freq = values._data, values.freq

        values = np.array(values, dtype="int64", copy=copy)
        self._data = values
        if freq is None:
            raise ValueError("freq is not specified and cannot be inferred")
        self._dtype = PeriodDtype(freq)
