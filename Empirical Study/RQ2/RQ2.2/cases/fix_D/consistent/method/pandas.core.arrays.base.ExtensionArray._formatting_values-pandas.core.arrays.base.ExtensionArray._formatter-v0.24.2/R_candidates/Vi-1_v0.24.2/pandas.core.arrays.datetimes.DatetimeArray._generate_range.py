    @classmethod
    def _generate_range(cls, start, end, periods, freq, tz=None,
                        normalize=False, ambiguous='raise',
                        nonexistent='raise', closed=None):

        periods = dtl.validate_periods(periods)
        if freq is None and any(x is None for x in [periods, start, end]):
            raise ValueError('Must provide freq argument if no data is '
                             'supplied')

        if com.count_not_none(start, end, periods, freq) != 3:
            raise ValueError('Of the four parameters: start, end, periods, '
                             'and freq, exactly three must be specified')
        freq = to_offset(freq)

        if start is not None:
            start = Timestamp(start)

        if end is not None:
            end = Timestamp(end)

        if start is None and end is None:
            if closed is not None:
                raise ValueError("Closed has to be None if not both of start"
                                 "and end are defined")
        if start is NaT or end is NaT:
            raise ValueError("Neither `start` nor `end` can be NaT")

        left_closed, right_closed = dtl.validate_endpoints(closed)

        start, end, _normalized = _maybe_normalize_endpoints(start, end,
                                                             normalize)

        tz = _infer_tz_from_endpoints(start, end, tz)

        if tz is not None:
            # Localize the start and end arguments
            start = _maybe_localize_point(
                start, getattr(start, 'tz', None), start, freq, tz
            )
            end = _maybe_localize_point(
                end, getattr(end, 'tz', None), end, freq, tz
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
            # TODO: consider re-implementing _cached_range; GH#17914
            values, _tz = generate_regular_range(start, end, periods, freq)
            index = cls._simple_new(values, freq=freq, dtype=tz_to_dtype(_tz))

            if tz is not None and index.tz is None:
                arr = conversion.tz_localize_to_utc(
                    index.asi8,
                    tz, ambiguous=ambiguous, nonexistent=nonexistent)

                index = cls(arr)

                # index is localized datetime64 array -> have to convert
                # start/end as well to compare
                if start is not None:
                    start = start.tz_localize(tz).asm8
                if end is not None:
                    end = end.tz_localize(tz).asm8
        else:
            # Create a linearly spaced date_range in local time
            # Nanosecond-granularity timestamps aren't always correctly
            # representable with doubles, so we limit the range that we
            # pass to np.linspace as much as possible
            arr = np.linspace(
                0, end.value - start.value,
                periods, dtype='int64') + start.value
            dtype = tz_to_dtype(tz)
            index = cls._simple_new(
                arr.astype('M8[ns]', copy=False), freq=None, dtype=dtype
            )

        if not left_closed and len(index) and index[0] == start:
            index = index[1:]
        if not right_closed and len(index) and index[-1] == end:
            index = index[:-1]

        dtype = tz_to_dtype(tz)
        return cls._simple_new(index.asi8, freq=freq, dtype=dtype)
