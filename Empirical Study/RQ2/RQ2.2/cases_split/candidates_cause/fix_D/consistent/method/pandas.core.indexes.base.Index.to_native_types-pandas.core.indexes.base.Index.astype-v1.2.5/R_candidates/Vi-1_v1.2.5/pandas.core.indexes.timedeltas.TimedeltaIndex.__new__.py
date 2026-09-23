    def __new__(
        cls,
        data=None,
        unit=None,
        freq=lib.no_default,
        closed=None,
        dtype=TD64NS_DTYPE,
        copy=False,
        name=None,
    ):
        name = maybe_extract_name(name, data, cls)

        if is_scalar(data):
            raise TypeError(
                f"{cls.__name__}() must be called with a "
                f"collection of some kind, {repr(data)} was passed"
            )

        if unit in {"Y", "y", "M"}:
            raise ValueError(
                "Units 'M', 'Y', and 'y' are no longer supported, as they do not "
                "represent unambiguous timedelta values durations."
            )

        if isinstance(data, TimedeltaArray) and freq is lib.no_default:
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name)

        if isinstance(data, TimedeltaIndex) and freq is lib.no_default and name is None:
            if copy:
                return data.copy()
            else:
                return data._shallow_copy()

        # - Cases checked above all return/raise before reaching here - #

        tdarr = TimedeltaArray._from_sequence_not_strict(
            data, freq=freq, unit=unit, dtype=dtype, copy=copy
        )
        return cls._simple_new(tdarr, name=name)
