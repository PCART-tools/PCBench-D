    @classmethod
    def _generate_range(
        cls,
        start,
        end,
        periods,
        freq,
        tz=None,
        normalize=False,
        ambiguous="raise",
        nonexistent="raise",
        inclusive="both",
    ):

        periods = dtl.validate_periods(periods)
        if freq is None and any(x is None for x in [periods, start, end]):
            raise ValueError("Must provide freq argument if no data is supplied")

        if com.count_not_none(start, end, periods, freq) != 3:
            raise ValueError(
                "Of the four parameters: start, end, periods, "
                "and freq, exactly three must be specified"
            )
        freq = to_offset(freq)

        if start is not None:
            start = Timestamp(start)

        if end is not None:
            end = Timestamp(end)

        if start is NaT or end is NaT:
            raise ValueError("Neither `start` nor `end` can be NaT")

        left_inclusive, right_inclusive = validate_inclusive(inclusive)
        start, end, _normalized = _maybe_normalize_endpoints(start, end, normalize)
        tz = _infer_tz_from_endpoints(start, end, tz)

        if tz is not None:
            # Localize the start and end arguments
            start_tz = None if start is None else start.tz
            end_tz = None if end is None else end.tz
            start = _maybe_localize_point(
                start, start_tz, start, freq, tz, ambiguous, nonexistent
            )
            end = _maybe_localize_point(
                end, end_tz, end, freq, tz, ambiguous, nonexistent
            )
        if freq is not None:
            # We break Day arithmetic (fixed 24 hour) here and opt for
            # Day to mean calendar day (23/24/25 hour). Therefore, strip
            # tz info from start and day to avoid DST arithmetic
            if isinstance(freq, Day):
                if start is not None:
                    start = start.tz_localize(None)
                if end is not None:
                    end = end.tz_localize(None)

            if isinstance(freq, Tick):
                i8values = generate_regular_range(start, end, periods, freq)
            else:
                xdr = generate_range(start=start, end=end, periods=periods, offset=freq)
                i8values = np.array([x.value for x in xdr], dtype=np.int64)

            endpoint_tz = start.tz if start is not None else end.tz

            if tz is not None and endpoint_tz is None:

                if not timezones.is_utc(tz):
                    # short-circuit tz_localize_to_utc which would make
                    #  an unnecessary copy with UTC but be a no-op.
                    i8values = tzconversion.tz_localize_to_utc(
                        i8values, tz, ambiguous=ambiguous, nonexistent=nonexistent
                    )

                # i8values is localized datetime64 array -> have to convert
                # start/end as well to compare
                if start is not None:
                    start = start.tz_localize(tz, ambiguous, nonexistent)
                if end is not None:
                    end = end.tz_localize(tz, ambiguous, nonexistent)
        else:
            # Create a linearly spaced date_range in local time
            # Nanosecond-granularity timestamps aren't always correctly
            # representable with doubles, so we limit the range that we
            # pass to np.linspace as much as possible
            i8values = (
                np.linspace(0, end.value - start.value, periods, dtype="int64")
                + start.value
            )
            if i8values.dtype != "i8":
                # 2022-01-09 I (brock) am not sure if it is possible for this
                #  to overflow and cast to e.g. f8, but if it does we need to cast
                i8values = i8values.astype("i8")

        if start == end:
            if not left_inclusive and not right_inclusive:
                i8values = i8values[1:-1]
        else:
            start_i8 = Timestamp(start).value
            end_i8 = Timestamp(end).value
            if not left_inclusive or not right_inclusive:
                if not left_inclusive and len(i8values) and i8values[0] == start_i8:
                    i8values = i8values[1:]
                if not right_inclusive and len(i8values) and i8values[-1] == end_i8:
                    i8values = i8values[:-1]

        dt64_values = i8values.view("datetime64[ns]")
        dtype = tz_to_dtype(tz)
        return cls._simple_new(dt64_values, freq=freq, dtype=dtype)
