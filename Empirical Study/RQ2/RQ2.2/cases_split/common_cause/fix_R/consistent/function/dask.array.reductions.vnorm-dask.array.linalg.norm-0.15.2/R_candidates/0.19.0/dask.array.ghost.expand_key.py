def expand_key(k, dims, name=None, axes=None):
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.expand_keys.',
         Warning)

    return overlap.expand_key(k, dims, name, axes)
