    def __new__(
        cls,
        data=None,
        ordinal=None,
        freq=None,
        start=None,
        end=None,
        periods=None,
        tz=None,
        dtype=None,
        copy=False,
        name=None,
        **fields
    ):

        valid_field_set = {
            "year",
            "month",
            "day",
            "quarter",
            "hour",
            "minute",
            "second",
        }

        if not set(fields).issubset(valid_field_set):
            raise TypeError(
                "__new__() got an unexpected keyword argument {}".format(
                    list(set(fields) - valid_field_set)[0]
                )
            )

        if name is None and hasattr(data, "name"):
            name = data.name

        if data is None and ordinal is None:
            # range-based.
            data, freq2 = PeriodArray._generate_range(start, end, periods, freq, fields)
            # PeriodArray._generate range does validate that fields is
            # empty when really using the range-based constructor.
            if not fields:
                msg = (
                    "Creating a PeriodIndex by passing range "
                    "endpoints is deprecated.  Use "
                    "`pandas.period_range` instead."
                )
                # period_range differs from PeriodIndex for cases like
                # start="2000", periods=4
                # PeriodIndex interprets that as A-DEC freq.
                # period_range interprets it as 'D' freq.
                cond = freq is None and (
                    (start and not isinstance(start, Period))
                    or (end and not isinstance(end, Period))
                )
                if cond:
                    msg += (
                        " Note that the default `freq` may differ. Pass "
                        "'freq=\"{}\"' to ensure the same output."
                    ).format(freq2.freqstr)
                warnings.warn(msg, FutureWarning, stacklevel=2)
            freq = freq2

            data = PeriodArray(data, freq=freq)
        else:
            freq = validate_dtype_freq(dtype, freq)

            # PeriodIndex allow PeriodIndex(period_index, freq=different)
            # Let's not encourage that kind of behavior in PeriodArray.

            if freq and isinstance(data, cls) and data.freq != freq:
                # TODO: We can do some of these with no-copy / coercion?
                # e.g. D -> 2D seems to be OK
                data = data.asfreq(freq)

            if data is None and ordinal is not None:
                # we strangely ignore `ordinal` if data is passed.
                ordinal = np.asarray(ordinal, dtype=np.int64)
                data = PeriodArray(ordinal, freq)
            else:
                # don't pass copy here, since we copy later.
                data = period_array(data=data, freq=freq)

        if copy:
            data = data.copy()

        return cls._simple_new(data, name=name)
