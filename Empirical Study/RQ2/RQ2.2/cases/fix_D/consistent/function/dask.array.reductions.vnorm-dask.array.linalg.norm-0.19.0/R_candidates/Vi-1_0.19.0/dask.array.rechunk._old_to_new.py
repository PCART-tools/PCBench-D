def _old_to_new(old_chunks, new_chunks):
    """ Helper to build old_chunks to new_chunks.

    Handles missing values, as long as the missing dimension
    is unchanged.

    Examples
    --------
    >>> old = ((10, 10, 10, 10, 10), )
    >>> new = ((25, 5, 20), )
    >>> _old_to_new(old, new)  # doctest: +NORMALIZE_WHITESPACE
    [[[(0, slice(0, 10, None)), (1, slice(0, 10, None)), (2, slice(0, 5, None))],
      [(2, slice(5, 10, None))],
      [(3, slice(0, 10, None)), (4, slice(0, 10, None))]]]
    """
    old_known = [x for x in old_chunks if not any(math.isnan(y) for y in x)]
    new_known = [x for x in new_chunks if not any(math.isnan(y) for y in x)]

    n_missing = [sum(math.isnan(y) for y in x) for x in old_chunks]
    n_missing2 = [sum(math.isnan(y) for y in x) for x in new_chunks]

    cmo = cumdims_label(old_known, 'o')
    cmn = cumdims_label(new_known, 'n')

    sums = [sum(o) for o in old_known]
    sums2 = [sum(n) for n in new_known]

    if not sums == sums2:
        raise ValueError('Cannot change dimensions from %r to %r' % (sums, sums2))
    if not n_missing == n_missing2:
        raise ValueError('Chunks must be unchanging along unknown dimensions')

    old_to_new = [_intersect_1d(_breakpoints(cm[0], cm[1])) for cm in zip(cmo, cmn)]
    for idx, missing in enumerate(n_missing):
        if missing:
            # Missing dimensions are always unchanged, so old -> new is everything
            extra = [[(i, slice(0, None))] for i in range(missing)]
            old_to_new.insert(idx, extra)
    return old_to_new
