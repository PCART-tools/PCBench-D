def length_of_indexer(indexer, target=None):
    """return the length of a single non-tuple indexer which could be a slice
    """
    if target is not None and isinstance(indexer, slice):
        l = len(target)
        start = indexer.start
        stop = indexer.stop
        step = indexer.step
        if start is None:
            start = 0
        elif start < 0:
            start += l
        if stop is None or stop > l:
            stop = l
        elif stop < 0:
            stop += l
        if step is None:
            step = 1
        elif step < 0:
            step = -step
        return (stop - start + step - 1) // step
    elif isinstance(indexer, (ABCSeries, Index, np.ndarray, list)):
        return len(indexer)
    elif not is_list_like_indexer(indexer):
        return 1
    raise AssertionError("cannot find the length of the indexer")
