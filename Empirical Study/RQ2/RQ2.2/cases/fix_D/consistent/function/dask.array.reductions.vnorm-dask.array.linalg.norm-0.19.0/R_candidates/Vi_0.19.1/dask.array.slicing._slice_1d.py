def _slice_1d(dim_shape, lengths, index):
    """Returns a dict of {blocknum: slice}

    This function figures out where each slice should start in each
    block for a single dimension. If the slice won't return any elements
    in the block, that block will not be in the output.

    Parameters
    ----------

    dim_shape - the number of elements in this dimension.
      This should be a positive, non-zero integer
    blocksize - the number of elements per block in this dimension
      This should be a positive, non-zero integer
    index - a description of the elements in this dimension that we want
      This might be an integer, a slice(), or an Ellipsis

    Returns
    -------

    dictionary where the keys are the integer index of the blocks that
      should be sliced and the values are the slices

    Examples
    --------

    Trivial slicing

    >>> _slice_1d(100, [60, 40], slice(None, None, None))
    {0: slice(None, None, None), 1: slice(None, None, None)}

    100 length array cut into length 20 pieces, slice 0:35

    >>> _slice_1d(100, [20, 20, 20, 20, 20], slice(0, 35))
    {0: slice(None, None, None), 1: slice(0, 15, 1)}

    Support irregular blocks and various slices

    >>> _slice_1d(100, [20, 10, 10, 10, 25, 25], slice(10, 35))
    {0: slice(10, 20, 1), 1: slice(None, None, None), 2: slice(0, 5, 1)}

    Support step sizes

    >>> _slice_1d(100, [15, 14, 13], slice(10, 41, 3))
    {0: slice(10, 15, 3), 1: slice(1, 14, 3), 2: slice(2, 12, 3)}

    >>> _slice_1d(100, [20, 20, 20, 20, 20], slice(0, 100, 40))  # step > blocksize
    {0: slice(0, 20, 40), 2: slice(0, 20, 40), 4: slice(0, 20, 40)}

    Also support indexing single elements

    >>> _slice_1d(100, [20, 20, 20, 20, 20], 25)
    {1: 5}

    And negative slicing

    >>> _slice_1d(100, [20, 20, 20, 20, 20], slice(100, 0, -3)) # doctest: +NORMALIZE_WHITESPACE
    {4: slice(-1, -21, -3),
     3: slice(-2, -21, -3),
     2: slice(-3, -21, -3),
     1: slice(-1, -21, -3),
     0: slice(-2, -20, -3)}

    >>> _slice_1d(100, [20, 20, 20, 20, 20], slice(100, 12, -3)) # doctest: +NORMALIZE_WHITESPACE
    {4: slice(-1, -21, -3),
     3: slice(-2, -21, -3),
     2: slice(-3, -21, -3),
     1: slice(-1, -21, -3),
     0: slice(-2, -8, -3)}

    >>> _slice_1d(100, [20, 20, 20, 20, 20], slice(100, -12, -3))
    {4: slice(-1, -12, -3)}
    """
    chunk_boundaries = np.cumsum(lengths, dtype=np.int64)

    if isinstance(index, Integral):
        # use right-side search to be consistent with previous result
        i = chunk_boundaries.searchsorted(index, side='right')
        if i > 0:
            # the very first chunk has no relative shift
            ind = index - chunk_boundaries[i - 1]
        else:
            ind = index
        return {int(i): int(ind)}

    assert isinstance(index, slice)

    if index == colon:
        return {k: colon for k in range(len(lengths))}

    step = index.step or 1
    if step > 0:
        start = index.start or 0
        stop = index.stop if index.stop is not None else dim_shape
    else:
        start = index.start if index.start is not None else dim_shape - 1
        start = dim_shape - 1 if start >= dim_shape else start
        stop = -(dim_shape + 1) if index.stop is None else index.stop

    # posify start and stop
    if start < 0:
        start += dim_shape
    if stop < 0:
        stop += dim_shape

    d = dict()
    if step > 0:
        istart = chunk_boundaries.searchsorted(start, side='right')
        istop = chunk_boundaries.searchsorted(stop, side='left')

        # the bound is not exactly tight; make it tighter?
        istop = min(istop + 1, len(lengths))

        # jump directly to istart
        if istart > 0:
            start = start - chunk_boundaries[istart - 1]
            stop = stop - chunk_boundaries[istart - 1]

        for i in range(istart, istop):
            length = lengths[i]
            if start < length and stop > 0:
                d[i] = slice(start, min(stop, length), step)
                start = (start - length) % step
            else:
                start = start - length
            stop -= length
    else:
        rstart = start  # running start

        istart = chunk_boundaries.searchsorted(start, side='left')
        istop = chunk_boundaries.searchsorted(stop, side='right')

        # the bound is not exactly tight; make it tighter?
        istart = min(istart + 1, len(chunk_boundaries) - 1)
        istop = max(istop - 1, -1)

        for i in range(istart, istop, -1):
            chunk_stop = chunk_boundaries[i]
            # create a chunk start and stop
            if i == 0:
                chunk_start = 0
            else:
                chunk_start = chunk_boundaries[i - 1]

            # if our slice is in this chunk
            if (chunk_start <= rstart < chunk_stop) and (rstart > stop):
                d[i] = slice(rstart - chunk_stop,
                             max(chunk_start - chunk_stop - 1,
                                 stop - chunk_stop),
                             step)

                # compute the next running start point,
                offset = (rstart - (chunk_start - 1)) % step
                rstart = chunk_start + offset - 1

    # replace 0:20:1 with : if appropriate
    for k, v in d.items():
        if v == slice(0, lengths[k], 1):
            d[k] = slice(None, None, None)

    if not d:  # special case x[:0]
        d[0] = slice(0, 0, 1)

    return d
