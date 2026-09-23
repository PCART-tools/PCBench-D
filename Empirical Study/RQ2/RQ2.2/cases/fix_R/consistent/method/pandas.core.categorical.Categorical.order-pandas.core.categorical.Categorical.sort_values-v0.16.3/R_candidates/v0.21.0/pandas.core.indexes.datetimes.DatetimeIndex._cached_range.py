    @classmethod
    def _cached_range(cls, start=None, end=None, periods=None, offset=None,
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

        if offset is None:
            # This can't happen with external-facing code
            raise TypeError('Must provide offset.')

        drc = _daterange_cache
        if offset not in _daterange_cache:
            xdr = generate_range(offset=offset, start=_CACHE_START,
                                 end=_CACHE_END)

            arr = tools.to_datetime(list(xdr), box=False)

            cachedRange = DatetimeIndex._simple_new(arr)
            cachedRange.offset = offset
            cachedRange.tz = None
            cachedRange.name = None
            drc[offset] = cachedRange
        else:
            cachedRange = drc[offset]

        if start is None:
            if not isinstance(end, Timestamp):
                raise AssertionError('end must be an instance of Timestamp')

            end = offset.rollback(end)

            endLoc = cachedRange.get_loc(end) + 1
            startLoc = endLoc - periods
        elif end is None:
            if not isinstance(start, Timestamp):
                raise AssertionError('start must be an instance of Timestamp')

            start = offset.rollforward(start)

            startLoc = cachedRange.get_loc(start)
            endLoc = startLoc + periods
        else:
            if not offset.onOffset(start):
                start = offset.rollforward(start)

            if not offset.onOffset(end):
                end = offset.rollback(end)

            startLoc = cachedRange.get_loc(start)
            endLoc = cachedRange.get_loc(end) + 1

        indexSlice = cachedRange[startLoc:endLoc]
        indexSlice.name = name
        indexSlice.offset = offset

        return indexSlice
