def nearest(x, axis, depth):
    """ Each reflect each boundary value outwards

    This mimics what the skimage.filters.gaussian_filter(... mode="nearest")
    does.
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.nearest.',
         Warning)

    return overlap.nearest(x, axis, depth)
