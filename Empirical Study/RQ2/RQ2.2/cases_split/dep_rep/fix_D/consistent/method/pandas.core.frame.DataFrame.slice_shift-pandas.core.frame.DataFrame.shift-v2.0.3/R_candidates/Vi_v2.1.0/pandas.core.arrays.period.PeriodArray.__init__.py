    def __init__(
        self, values, dtype: Dtype | None = None, freq=None, copy: bool = False
    ) -> None:
        if freq is not None:
            # GH#52462
            warnings.warn(
                "The 'freq' keyword in the PeriodArray constructor is deprecated "
                "and will be removed in a future version. Pass 'dtype' instead",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            freq = validate_dtype_freq(dtype, freq)
            dtype = PeriodDtype(freq)

        if dtype is not None:
            dtype = pandas_dtype(dtype)
            if not isinstance(dtype, PeriodDtype):
                raise ValueError(f"Invalid dtype {dtype} for PeriodArray")

        if isinstance(values, ABCSeries):
            values = values._values
            if not isinstance(values, type(self)):
                raise TypeError("Incorrect dtype")

        elif isinstance(values, ABCPeriodIndex):
            values = values._values

        if isinstance(values, type(self)):
            if dtype is not None and dtype != values.dtype:
                raise raise_on_incompatible(values, dtype.freq)
            values, dtype = values._ndarray, values.dtype

        values = np.array(values, dtype="int64", copy=copy)
        if dtype is None:
            raise ValueError("dtype is not specified and cannot be inferred")
        dtype = cast(PeriodDtype, dtype)
        NDArrayBacked.__init__(self, values, dtype)
