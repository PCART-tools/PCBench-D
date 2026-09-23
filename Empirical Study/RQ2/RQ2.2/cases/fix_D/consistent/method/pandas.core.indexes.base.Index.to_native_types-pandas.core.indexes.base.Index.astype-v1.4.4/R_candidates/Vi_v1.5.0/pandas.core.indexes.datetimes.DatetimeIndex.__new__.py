    def __new__(
        cls,
        data=None,
        freq: str | BaseOffset | lib.NoDefault = lib.no_default,
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

        if (
            isinstance(data, DatetimeArray)
            and freq is lib.no_default
            and tz is None
            and dtype is None
        ):
            # fastpath, similar logic in TimedeltaIndex.__new__;
            # Note in this particular case we retain non-nano.
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name)
        elif (
            isinstance(data, DatetimeArray)
            and freq is lib.no_default
            and tz is None
            and is_dtype_equal(data.dtype, dtype)
        ):
            # Reached via Index.__new__ when we call .astype
            # TODO(2.0): special casing can be removed once _from_sequence_not_strict
            #  no longer chokes on non-nano
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name)

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
