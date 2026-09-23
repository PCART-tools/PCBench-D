def add_dummy_padding(x, depth, boundary):
    """
    Pads an array which has 'none' as the boundary type.
    Used to simplify trimming arrays which use 'none'.

    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)
    >>> add_dummy_padding(x, {0: 1}, {0: 'none'}).compute()  # doctest: +NORMALIZE_WHITESPACE
    array([..., 0, 1, 2, 3, 4, 5, ...])
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.add_dummy_padding.',
         Warning)

    return overlap.add_dummy_padding(x, depth, boundary)
