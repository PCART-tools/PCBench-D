def _intersect_1d(breaks):
    """
    Internal utility to intersect chunks for 1d after preprocessing.

    >>> new = cumdims_label(((2, 3), (2, 2, 1)), 'n')
    >>> old = cumdims_label(((2, 2, 1), (5,)), 'o')

    >>> _intersect_1d(_breakpoints(old[0], new[0]))  # doctest: +NORMALIZE_WHITESPACE
    [[(0, slice(0, 2, None))],
     [(1, slice(0, 2, None)), (2, slice(0, 1, None))]]
    >>> _intersect_1d(_breakpoints(old[1], new[1]))  # doctest: +NORMALIZE_WHITESPACE
    [[(0, slice(0, 2, None))],
     [(0, slice(2, 4, None))],
     [(0, slice(4, 5, None))]]

    Parameters
    ----------

    breaks: list of tuples
        Each tuple is ('o', 8) or ('n', 8)
        These are pairs of 'o' old or new 'n'
        indicator with a corresponding cumulative sum.

    Uses 'o' and 'n' to make new tuples of slices for
    the new block crosswalk to old blocks.
    """
    start = 0
    last_end = 0
    old_idx = 0
    ret = []
    ret_next = []
    for idx in range(1, len(breaks)):
        label, br = breaks[idx]
        last_label, last_br = breaks[idx - 1]
        if last_label == 'n':
            if ret_next:
                ret.append(ret_next)
                ret_next = []
        if last_label == 'o':
            start = 0
        else:
            start = last_end
        end = br - last_br + start
        last_end = end
        if br == last_br:
            continue
        ret_next.append((old_idx, slice(start, end)))
        if label == 'o':
            old_idx += 1
            start = 0

    if ret_next:
        ret.append(ret_next)

    return ret
