def _intersect_1d(breaks):
    """
    Internal utility to intersect chunks for 1d after preprocessing.

    >>> new = cumdims_label(((2, 3), (2, 2, 1)), 'n')
    >>> old = cumdims_label(((2, 2, 1), (5,)), 'o')

    >>> _intersect_1d(_breakpoints(old[0], new[0]))  # doctest: +NORMALIZE_WHITESPACE
    (((0, slice(0, 2, None)),),
     ((1, slice(0, 2, None)), (2, slice(0, 1, None))))
    >>> _intersect_1d(_breakpoints(old[1], new[1]))  # doctest: +NORMALIZE_WHITESPACE
    (((0, slice(0, 2, None)),),
     ((0, slice(2, 4, None)),),
     ((0, slice(4, 5, None)),))

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
    lastbi = ('n',0)
    ret = [[]]
    for idx in range(1, len(breaks)):
        bi = breaks[idx]
        lastbi = breaks[idx -1]
        if 'n' in lastbi[0] and bi[1]:
            ret.append([])
        if 'o' in lastbi[0]:
            start = 0
        else:
            start = last_end
        end = bi[1] - lastbi[1] + start
        last_end = end
        if bi[1] == lastbi[1]:
            continue
        ret[-1].append((old_idx, slice(start, end)))
        if bi[0] == 'o':
            old_idx += 1
            start = 0
    return tuple(map(tuple, filter(None, ret)))
