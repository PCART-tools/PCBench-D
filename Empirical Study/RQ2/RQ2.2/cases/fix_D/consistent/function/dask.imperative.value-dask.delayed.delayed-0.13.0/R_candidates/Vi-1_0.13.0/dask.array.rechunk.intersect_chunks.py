def intersect_chunks(old_chunks, new_chunks):
    """
    Make dask.array slices as intersection of old and new chunks.

    >>> intersections = intersect_chunks(((4, 4), (2,)),
    ...                                  ((8,), (1, 1)))
    >>> list(intersections)  # doctest: +NORMALIZE_WHITESPACE
    [(((0, slice(0, 4, None)), (0, slice(0, 1, None))),
      ((1, slice(0, 4, None)), (0, slice(0, 1, None)))),
     (((0, slice(0, 4, None)), (0, slice(1, 2, None))),
      ((1, slice(0, 4, None)), (0, slice(1, 2, None))))]

    Parameters
    ----------

    old_chunks : iterable of tuples
        block sizes along each dimension (convert from old_chunks)
    new_chunks: iterable of tuples
        block sizes along each dimension (converts to new_chunks)
    """
    cmo = cumdims_label(old_chunks, 'o')
    cmn = cumdims_label(new_chunks, 'n')
    sums = [sum(o) for o in old_chunks]
    sums2 = [sum(n) for n in old_chunks]
    if not sums == sums2:
        raise ValueError('Cannot change dimensions from to %r' % sums2)
    old_to_new = [_intersect_1d(_breakpoints(cm[0], cm[1]))
                  for cm in zip(cmo, cmn)]
    cross1 = product(*old_to_new)
    cross = chain(tuple(product(*cr)) for cr in cross1)
    return cross
