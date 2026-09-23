def reflect(x, axis, depth):
    """ Reflect boundaries of array on the same side

    This is the converse of ``periodic``
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.reflect.',
         Warning)

    return overlap.reflect(x, axis, depth)
