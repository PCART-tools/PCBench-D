def ghost_internal(x, axes):
    """ Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    axes: dict
        The size of the shared boundary per axis

    The axes input informs how many cells to dask.array.overlap between neighboring blocks
    {0: 2, 2: 5} means share two cells in 0 axis, 5 cells in 2 axis
    """
    warn('DeprecationWarning: the dask.array.ghost module has '
         'been renamed to dask.array.overlap, '
         'use dask.array.overlap.ghost_internal.',
         Warning)

    return overlap.overlap_internal(x, axes)
