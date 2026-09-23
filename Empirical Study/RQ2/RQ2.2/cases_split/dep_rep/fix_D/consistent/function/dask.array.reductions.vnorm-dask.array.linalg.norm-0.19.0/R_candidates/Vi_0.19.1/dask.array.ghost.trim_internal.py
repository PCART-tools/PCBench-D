def trim_internal(x, axes):
    """ Trim sides from each block

    This couples well with the ghost operation, which may leave excess data on
    each block

    See also
    --------
    dask.array.chunk.trim
    dask.array.map_blocks
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.trim_internal.',
         Warning)

    return overlap.trim_internal(x, axes)
