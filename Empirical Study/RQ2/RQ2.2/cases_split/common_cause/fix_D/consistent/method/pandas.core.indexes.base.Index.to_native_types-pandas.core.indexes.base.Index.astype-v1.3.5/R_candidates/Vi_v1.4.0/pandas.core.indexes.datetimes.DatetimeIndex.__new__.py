    def __new__(
        cls,
        data=None,
        freq=lib.no_default,
        tz=None,
        normalize: bool = False,
        closed=None,
        ambiguous="raise",
        dayfirst: bool = False,
        yearfirst: bool = False,
        dtype: Dtype | None = None,
        copy: bool = False,
        name: Hashable = None,
    ) -> DatetimeIndex:

        if is_scalar(data):
            raise cls._scalar_data_error(data)

        # - Cases checked above all return/raise before reaching here - #

        name = maybe_extract_name(name, data, cls)

        dtarr = DatetimeArray._from_sequence_not_strict(
            data,
            dtype=dtype,
            copy=copy,
            tz=tz,
            freq=freq,
            dayfirst=dayfirst,
            yearfirst=yearfirst,
            ambiguous=ambiguous,
        )

        subarr = cls._simple_new(dtarr, name=name)
        return subarr
