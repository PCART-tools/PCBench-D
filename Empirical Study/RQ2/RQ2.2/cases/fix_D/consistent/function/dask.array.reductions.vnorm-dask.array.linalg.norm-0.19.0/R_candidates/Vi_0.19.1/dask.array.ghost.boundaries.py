def boundaries(x, depth=None, kind=None):
    """ Add boundary conditions to an array before ghosting

    See Also
    --------
    periodic
    constant
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.boundaries.',
         Warning)

    return overlap.boundaries(x, depth, kind)
