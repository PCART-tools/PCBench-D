    @classmethod
    def _from_sequence_not_strict(
        cls,
        data,
        dtype=TD64NS_DTYPE,
        copy: bool = False,
        freq=lib.no_default,
        unit=None,
    ) -> TimedeltaArray:
        if dtype:
            _validate_td64_dtype(dtype)

        explicit_none = freq is None
        freq = freq if freq is not lib.no_default else None

        freq, freq_infer = dtl.maybe_infer_freq(freq)

        data, inferred_freq = sequence_to_td64ns(data, copy=copy, unit=unit)
        freq, freq_infer = dtl.validate_inferred_freq(freq, inferred_freq, freq_infer)
        if explicit_none:
            freq = None

        result = cls._simple_new(data, freq=freq)

        if inferred_freq is None and freq is not None:
            # this condition precludes `freq_infer`
            cls._validate_frequency(result, freq)

        elif freq_infer:
            # Set _freq directly to bypass duplicative _validate_frequency
            # check.
            result._freq = to_offset(result.inferred_freq)

        return result
