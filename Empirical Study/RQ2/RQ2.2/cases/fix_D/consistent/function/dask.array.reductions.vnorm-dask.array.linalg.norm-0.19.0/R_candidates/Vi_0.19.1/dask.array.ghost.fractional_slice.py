def fractional_slice(task, axes):
    """

    >>> fractional_slice(('x', 5.1), {0: 2})  # doctest: +SKIP
    (getitem, ('x', 6), (slice(0, 2),))

    >>> fractional_slice(('x', 3, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(None, None, None), slice(-3, None)))

    >>> fractional_slice(('x', 2.9, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(0, 2), slice(-3, None)))
    """

    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.fractional_slice.',
         Warning)

    return overlap.fractional_slice(task, axes)
