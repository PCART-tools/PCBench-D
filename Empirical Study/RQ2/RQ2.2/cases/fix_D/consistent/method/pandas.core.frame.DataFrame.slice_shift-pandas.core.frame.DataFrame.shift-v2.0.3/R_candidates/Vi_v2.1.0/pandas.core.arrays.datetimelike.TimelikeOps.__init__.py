    def __init__(
        self, values, dtype=None, freq=lib.no_default, copy: bool = False
    ) -> None:
        values = extract_array(values, extract_numpy=True)
        if isinstance(values, IntegerArray):
            values = values.to_numpy("int64", na_value=iNaT)

        inferred_freq = getattr(values, "_freq", None)
        explicit_none = freq is None
        freq = freq if freq is not lib.no_default else None

        if isinstance(values, type(self)):
            if explicit_none:
                # don't inherit from values
                pass
            elif freq is None:
                freq = values.freq
            elif freq and values.freq:
                freq = to_offset(freq)
                freq, _ = validate_inferred_freq(freq, values.freq, False)

            if dtype is not None:
                dtype = pandas_dtype(dtype)
                if dtype != values.dtype:
                    # TODO: we only have tests for this for DTA, not TDA (2022-07-01)
                    raise TypeError(
                        f"dtype={dtype} does not match data dtype {values.dtype}"
                    )

            dtype = values.dtype
            values = values._ndarray

        elif dtype is None:
            if isinstance(values, np.ndarray) and values.dtype.kind in "Mm":
                dtype = values.dtype
            else:
                dtype = self._default_dtype

        if not isinstance(values, np.ndarray):
            raise ValueError(
                f"Unexpected type '{type(values).__name__}'. 'values' must be a "
                f"{type(self).__name__}, ndarray, or Series or Index "
                "containing one of those."
            )
        if values.ndim not in [1, 2]:
            raise ValueError("Only 1-dimensional input arrays are supported.")

        if values.dtype == "i8":
            # for compat with datetime/timedelta/period shared methods,
            #  we can sometimes get here with int64 values.  These represent
            #  nanosecond UTC (or tz-naive) unix timestamps
            values = values.view(self._default_dtype)

        dtype = self._validate_dtype(values, dtype)

        if freq == "infer":
            raise ValueError(
                f"Frequency inference not allowed in {type(self).__name__}.__init__. "
                "Use 'pd.array()' instead."
            )

        if copy:
            values = values.copy()
        if freq:
            freq = to_offset(freq)
            if values.dtype.kind == "m" and not isinstance(freq, Tick):
                raise TypeError("TimedeltaArray/Index freq must be a Tick")

        NDArrayBacked.__init__(self, values=values, dtype=dtype)
        self._freq = freq

        if inferred_freq is None and freq is not None:
            type(self)._validate_frequency(self, freq)
