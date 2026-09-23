    @classmethod
    def _from_sequence(cls, data, *, dtype=None, copy: bool = False) -> TimedeltaArray:
        if dtype:
            dtype = _validate_td64_dtype(dtype)

        data, inferred_freq = sequence_to_td64ns(data, copy=copy, unit=None)
        freq, _ = dtl.validate_inferred_freq(None, inferred_freq, False)

        if dtype is not None:
            data = astype_overflowsafe(data, dtype=dtype, copy=False)

        return cls._simple_new(data, dtype=data.dtype, freq=freq)
