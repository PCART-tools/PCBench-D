def concatenate(seq, axis=0):
    """
    Concatenate arrays along an existing axis

    Given a sequence of dask Arrays form a new dask Array by stacking them
    along an existing dimension (axis=0 by default)

    Examples
    --------

    Create slices

    >>> import dask.array as da
    >>> import numpy as np

    >>> data = [from_array(np.ones((4, 4)), chunks=(2, 2))
    ...          for i in range(3)]

    >>> x = da.concatenate(data, axis=0)
    >>> x.shape
    (12, 4)

    >>> da.concatenate(data, axis=1).shape
    (4, 12)

    Result is a new dask Array

    See Also
    --------
    stack
    """
    n = len(seq)
    ndim = len(seq[0].shape)
    if axis < 0:
        axis = ndim + axis
    if axis >= ndim:
        msg = ("Axis must be less than than number of dimensions"
               "\nData has %d dimensions, but got axis=%d")
        raise ValueError(msg % (ndim, axis))

    inds = [list(range(ndim)) for i in range(n)]
    for i, ind in enumerate(inds):
        ind[axis] = -(i + 1)

    uc_args = list(concat(zip(seq, inds)))
    _, seq = unify_chunks(*uc_args, warn=False)

    bds = [a.chunks for a in seq]

    chunks = (seq[0].chunks[:axis] + (sum([bd[axis] for bd in bds], ()), ) +
              seq[0].chunks[axis + 1:])

    cum_dims = [0] + list(accumulate(add, [len(a.chunks[axis]) for a in seq]))

    dt = reduce(np.promote_types, [a.dtype for a in seq])
    seq = [x.astype(dt) for x in seq]

    names = [a.name for a in seq]

    name = 'concatenate-' + tokenize(names, axis)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))

    values = [(names[bisect(cum_dims, key[axis + 1]) - 1],) + key[1:axis + 1] +
              (key[axis + 1] - cum_dims[bisect(cum_dims, key[axis + 1]) - 1], ) +
              key[axis + 2:] for key in keys]

    dsk = dict(zip(keys, values))
    dsk2 = sharedict.merge((name, dsk), * [a.dask for a in seq])

    return Array(dsk2, name, chunks, dtype=dt)
