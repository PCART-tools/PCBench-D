def overlap_internal(x, axes):
    """ Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    axes: dict
        The size of the shared boundary per axis

    The axes input informs how many cells to overlap between neighboring blocks
    {0: 2, 2: 5} means share two cells in 0 axis, 5 cells in 2 axis
    """
    dims = list(map(len, x.chunks))
    expand_key2 = partial(expand_key, dims=dims, axes=axes)

    # Make keys for each of the surrounding sub-arrays
    interior_keys = pipe(x.__dask_keys__(), flatten, map(expand_key2),
                         map(flatten), concat, list)

    name = 'overlap-' + tokenize(x, axes)
    getitem_name = 'getitem-' + tokenize(x, axes)
    interior_slices = {}
    overlap_blocks = {}
    for k in interior_keys:
        frac_slice = fractional_slice((x.name,) + k, axes)
        if (x.name,) + k != frac_slice:
            interior_slices[(getitem_name,) + k] = frac_slice
        else:
            interior_slices[(getitem_name,) + k] = (x.name,) + k
            overlap_blocks[(name,) + k] = (concatenate3,
                                           (concrete, expand_key2((None,) + k, name=getitem_name)))

    chunks = []
    for i, bds in enumerate(x.chunks):
        if len(bds) == 1:
            chunks.append(bds)
        else:
            left = [bds[0] + axes.get(i, 0)]
            right = [bds[-1] + axes.get(i, 0)]
            mid = []
            for bd in bds[1:-1]:
                mid.append(bd + axes.get(i, 0) * 2)
            chunks.append(left + mid + right)

    dsk = merge(interior_slices, overlap_blocks)
    dsk = sharedict.merge(x.dask, (name, dsk))

    return Array(dsk, name, chunks, dtype=x.dtype)
