    def __new__(
        cls,
        data=None,
        unit=None,
        freq=lib.no_default,
        closed=None,
        dtype=None,
        copy: bool = False,
        name=None,
    ):
        name = maybe_extract_name(name, data, cls)

        if is_scalar(data):
            cls._raise_scalar_data_error(data)

        if unit in {"Y", "y", "M"}:
            raise ValueError(
                "Units 'M', 'Y', and 'y' are no longer supported, as they do not "
                "represent unambiguous timedelta values durations."
            )

        if (
            isinstance(data, TimedeltaArray)
            and freq is lib.no_default
            and (dtype is None or is_dtype_equal(dtype, data.dtype))
        ):
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name)

        if (
            isinstance(data, TimedeltaIndex)
            and freq is lib.no_default
            and name is None
            and (dtype is None or is_dtype_equal(dtype, data.dtype))
        ):
            if copy:
                return data.copy()
            else:
                return data._view()

        # - Cases checked above all return/raise before reaching here - #

        tdarr = TimedeltaArray._from_sequence_not_strict(
            data, freq=freq, unit=unit, dtype=dtype, copy=copy
        )
        refs = None
        if not copy and isinstance(data, (ABCSeries, Index)):
            refs = data._references

        return cls._simple_new(tdarr, name=name, refs=refs)
