def coerce_boundary(ndim, boundary):
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.coerce_boundary.',
         Warning)

    return overlap.coerce_boundary(ndim, boundary)
