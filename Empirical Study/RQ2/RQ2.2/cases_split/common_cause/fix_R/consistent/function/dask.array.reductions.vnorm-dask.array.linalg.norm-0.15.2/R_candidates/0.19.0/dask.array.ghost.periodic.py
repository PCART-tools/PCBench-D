def periodic(x, axis, depth):
    """ Copy a slice of an array around to its other side

    Useful to create periodic boundary conditions for ghost
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.periodic.',
         Warning)

    return overlap.periodic(x, axis, depth)
