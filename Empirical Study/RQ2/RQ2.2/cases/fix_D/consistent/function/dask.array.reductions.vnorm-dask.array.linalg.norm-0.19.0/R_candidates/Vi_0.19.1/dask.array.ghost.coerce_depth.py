def coerce_depth(ndim, depth):
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.coerce_depth.',
         Warning)

    return overlap.coerce_depth(ndim, depth)
