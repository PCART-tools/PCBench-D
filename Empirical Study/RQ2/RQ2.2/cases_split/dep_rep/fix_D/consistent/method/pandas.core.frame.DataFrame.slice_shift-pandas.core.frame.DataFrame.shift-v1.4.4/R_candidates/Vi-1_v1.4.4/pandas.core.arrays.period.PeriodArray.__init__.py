    def __init__(
        self, values, dtype: Dtype | None = None, freq=None, copy: bool = False
    ):
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
                raise raise_on_incompatible(values, freq)
            values, freq = values._ndarray, values.freq

        values = np.array(values, dtype="int64", copy=copy)
        if freq is None:
            raise ValueError("freq is not specified and cannot be inferred")
        NDArrayBacked.__init__(self, values, PeriodDtype(freq))
