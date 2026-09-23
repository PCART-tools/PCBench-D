def _maybe_partial_time_string(index, indexer, kind):
    """
    Convert indexer for partial string selection
    if data has DatetimeIndex/PeriodIndex
    """
    # do not pass dd.Index
    assert isinstance(index, pd.Index)

    if not isinstance(index, (pd.DatetimeIndex, pd.PeriodIndex)):
        return indexer

    if isinstance(indexer, slice):
        if isinstance(indexer.start, pd.compat.string_types):
            start = index._maybe_cast_slice_bound(indexer.start, 'left', kind)
        else:
            start = indexer.start

        if isinstance(indexer.stop, pd.compat.string_types):
            stop = index._maybe_cast_slice_bound(indexer.stop, 'right', kind)
        else:
            stop = indexer.stop
        return slice(start, stop)

    elif isinstance(indexer, pd.compat.string_types):
        start = index._maybe_cast_slice_bound(indexer, 'left', 'loc')
        stop = index._maybe_cast_slice_bound(indexer, 'right', 'loc')
        return slice(min(start, stop), max(start, stop))

    return indexer
