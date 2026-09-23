    @classmethod
    def _cached_range(cls, start=None, end=None, periods=None, freq=None,
                      name=None):
        if start is None and end is None:
            # I somewhat believe this should never be raised externally
            raise TypeError('Must specify either start or end.')
        if start is not None:
            start = Timestamp(start)
        if end is not None:
            end = Timestamp(end)
        if (start is None or end is None) and periods is None:
            raise TypeError(
                'Must either specify period or provide both start and end.')

        if freq is None:
            # This can't happen with external-facing code
            raise TypeError('Must provide freq.')

        drc = _daterange_cache
        if freq not in _daterange_cache:
            xdr = generate_range(offset=freq, start=_CACHE_START,
                                 end=_CACHE_END)

            arr = tools.to_datetime(list(xdr), box=False)

            cachedRange = DatetimeIndex._simple_new(arr)
            cachedRange.freq = freq
            cachedRange = cachedRange.tz_localize(None)
            cachedRange.name = None
            drc[freq] = cachedRange
        else:
            cachedRange = drc[freq]

        if start is None:
            if not isinstance(end, Timestamp):
                raise AssertionError('end must be an instance of Timestamp')

            end = freq.rollback(end)

            endLoc = cachedRange.get_loc(end) + 1
            startLoc = endLoc - periods
        elif end is None:
            if not isinstance(start, Timestamp):
                raise AssertionError('start must be an instance of Timestamp')

            start = freq.rollforward(start)

            startLoc = cachedRange.get_loc(start)
            endLoc = startLoc + periods
        else:
            if not freq.onOffset(start):
                start = freq.rollforward(start)

            if not freq.onOffset(end):
                end = freq.rollback(end)

            startLoc = cachedRange.get_loc(start)
            endLoc = cachedRange.get_loc(end) + 1

        indexSlice = cachedRange[startLoc:endLoc]
        indexSlice.name = name
        indexSlice.freq = freq

        return indexSlice
