def constant(x, axis, depth, value):
    """ Add constant slice to either side of array """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.constant.',
         Warning)

    return overlap.constant(x, axis, depth, value)
