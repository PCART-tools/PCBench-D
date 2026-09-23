    @classmethod
    def _from_sequence_not_strict(
        cls,
        data,
        *,
        dtype=None,
        copy: bool = False,
        tz=lib.no_default,
        freq: str | BaseOffset | lib.NoDefault | None = lib.no_default,
        dayfirst: bool = False,
        yearfirst: bool = False,
        ambiguous: TimeAmbiguous = "raise",
    ):
        """
        A non-strict version of _from_sequence, called from DatetimeIndex.__new__.
        """
        explicit_none = freq is None
        freq = freq if freq is not lib.no_default else None
        freq, freq_infer = dtl.maybe_infer_freq(freq)

        # if the user either explicitly passes tz=None or a tz-naive dtype, we
        #  disallows inferring a tz.
        explicit_tz_none = tz is None
        if tz is lib.no_default:
            tz = None
        else:
            tz = timezones.maybe_get_tz(tz)

        dtype = _validate_dt64_dtype(dtype)
        # if dtype has an embedded tz, capture it
        tz = _validate_tz_from_dtype(dtype, tz, explicit_tz_none)

        unit = None
        if dtype is not None:
            if isinstance(dtype, np.dtype):
                unit = np.datetime_data(dtype)[0]
            else:
                # DatetimeTZDtype
                unit = dtype.unit

        subarr, tz, inferred_freq = _sequence_to_dt64ns(
            data,
            copy=copy,
            tz=tz,
            dayfirst=dayfirst,
            yearfirst=yearfirst,
            ambiguous=ambiguous,
            out_unit=unit,
        )
        # We have to call this again after possibly inferring a tz above
        _validate_tz_from_dtype(dtype, tz, explicit_tz_none)
        if tz is not None and explicit_tz_none:
            raise ValueError(
                "Passed data is timezone-aware, incompatible with 'tz=None'. "
                "Use obj.tz_localize(None) instead."
            )

        freq, freq_infer = dtl.validate_inferred_freq(freq, inferred_freq, freq_infer)
        if explicit_none:
            freq = None

        data_unit = np.datetime_data(subarr.dtype)[0]
        data_dtype = tz_to_dtype(tz, data_unit)
        result = cls._simple_new(subarr, freq=freq, dtype=data_dtype)
        if unit is not None and unit != result.unit:
            # If unit was specified in user-passed dtype, cast to it here
            result = result.as_unit(unit)

        if inferred_freq is None and freq is not None:
            # this condition precludes `freq_infer`
            cls._validate_frequency(result, freq, ambiguous=ambiguous)

        elif freq_infer:
            # Set _freq directly to bypass duplicative _validate_frequency
            # check.
            result._freq = to_offset(result.inferred_freq)

        return result
