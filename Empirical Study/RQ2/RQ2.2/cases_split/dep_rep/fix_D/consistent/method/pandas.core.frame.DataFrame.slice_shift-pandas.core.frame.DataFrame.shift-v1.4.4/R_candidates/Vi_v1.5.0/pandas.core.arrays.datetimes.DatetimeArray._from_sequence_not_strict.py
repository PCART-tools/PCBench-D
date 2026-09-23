    @classmethod
    def _from_sequence_not_strict(
        cls,
        data,
        dtype=None,
        copy: bool = False,
        tz=None,
        freq: str | BaseOffset | lib.NoDefault | None = lib.no_default,
        dayfirst: bool = False,
        yearfirst: bool = False,
        ambiguous="raise",
    ):
        explicit_none = freq is None
        freq = freq if freq is not lib.no_default else None

        freq, freq_infer = dtl.maybe_infer_freq(freq)

        subarr, tz, inferred_freq = _sequence_to_dt64ns(
            data,
            dtype=dtype,
            copy=copy,
            tz=tz,
            dayfirst=dayfirst,
            yearfirst=yearfirst,
            ambiguous=ambiguous,
        )

        freq, freq_infer = dtl.validate_inferred_freq(freq, inferred_freq, freq_infer)
        if explicit_none:
            freq = None

        dtype = tz_to_dtype(tz)
        result = cls._simple_new(subarr, freq=freq, dtype=dtype)

        if inferred_freq is None and freq is not None:
            # this condition precludes `freq_infer`
            cls._validate_frequency(result, freq, ambiguous=ambiguous)

        elif freq_infer:
            # Set _freq directly to bypass duplicative _validate_frequency
            # check.
            result._freq = to_offset(result.inferred_freq)

        return result
