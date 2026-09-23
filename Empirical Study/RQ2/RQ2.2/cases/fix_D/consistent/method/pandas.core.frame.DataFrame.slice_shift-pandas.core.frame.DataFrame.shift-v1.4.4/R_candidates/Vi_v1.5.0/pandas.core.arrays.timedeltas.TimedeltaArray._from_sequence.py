    @classmethod
    def _from_sequence(
        cls, data, *, dtype=TD64NS_DTYPE, copy: bool = False
    ) -> TimedeltaArray:
        if dtype:
            _validate_td64_dtype(dtype)

        data, inferred_freq = sequence_to_td64ns(data, copy=copy, unit=None)
        freq, _ = dtl.validate_inferred_freq(None, inferred_freq, False)

        return cls._simple_new(data, dtype=data.dtype, freq=freq)
