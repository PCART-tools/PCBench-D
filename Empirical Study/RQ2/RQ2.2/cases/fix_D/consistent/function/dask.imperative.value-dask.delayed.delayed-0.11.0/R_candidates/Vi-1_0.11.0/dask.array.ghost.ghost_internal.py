def ghost_internal(x, axes):
    """ Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    axes: dict
        The size of the shared boundary per axis

    The axes dict informs how many cells to overlap between neighboring blocks
    {0: 2, 2: 5} means share two cells in 0 axis, 5 cells in 2 axis
    """
    dims = list(map(len, x.chunks))
    expand_key2 = partial(expand_key, dims=dims)
    interior_keys = pipe(x._keys(), flatten, map(expand_key2), map(flatten),
                         concat, list)

    token = tokenize(x, axes)
    name = 'ghost-' + token
    interior_slices = {}
    ghost_blocks = {}
    for k in interior_keys:
        frac_slice = fractional_slice(k, axes)
        if k != frac_slice:
            interior_slices[k] = frac_slice

        ghost_blocks[(name,) + k[1:]] = (concatenate3,
                                          (concrete, expand_key2(k)))

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

    return Array(merge(interior_slices, ghost_blocks, x.dask),
                 name, chunks)
