def trim_internal(x, axes):
    """ Trim sides from each block

    This couples well with the overlap operation, which may leave excess data on
    each block

    See also
    --------
    dask.array.chunk.trim
    dask.array.map_blocks
    """
    olist = []
    for i, bd in enumerate(x.chunks):
        ilist = []
        for d in bd:
            ilist.append(d - axes.get(i, 0) * 2)
        olist.append(tuple(ilist))

    chunks = tuple(olist)

    return map_blocks(partial(chunk.trim, axes=axes), x, chunks=chunks,
                      dtype=x.dtype)
