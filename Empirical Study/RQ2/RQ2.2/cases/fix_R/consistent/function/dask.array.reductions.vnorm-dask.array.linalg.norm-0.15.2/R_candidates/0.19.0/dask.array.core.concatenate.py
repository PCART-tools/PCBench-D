def concatenate(seq, axis=0, allow_unknown_chunksizes=False):
    """
    Concatenate arrays along an existing axis

    Given a sequence of dask Arrays form a new dask Array by stacking them
    along an existing dimension (axis=0 by default)

    Parameters
    ----------
    seq: list of dask.arrays
    axis: int
        Dimension along which to align all of the arrays
    allow_unknown_chunksizes: bool
        Allow unknown chunksizes, such as come from converting from dask
        dataframes.  Dask.array is unable to verify that chunks line up.  If
        data comes from differently aligned sources then this can cause
        unexpected results.

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

    if n == 1:
        return seq[0]

    if (not allow_unknown_chunksizes and
        not all(i == axis or all(x.shape[i] == seq[0].shape[i] for x in seq)
                for i in range(ndim))):
        if any(map(np.isnan, seq[0].shape)):
            raise ValueError("Tried to concatenate arrays with unknown"
                             " shape %s.  To force concatenation pass"
                             " allow_unknown_chunksizes=True."
                             % str(seq[0].shape))
        raise ValueError("Shapes do not align: %s", [x.shape for x in seq])

    inds = [list(range(ndim)) for i in range(n)]
    for i, ind in enumerate(inds):
        ind[axis] = -(i + 1)

    uc_args = list(concat(zip(seq, inds)))
    _, seq = unify_chunks(*uc_args, warn=False)

    bds = [a.chunks for a in seq]

    chunks = (seq[0].chunks[:axis] + (sum([bd[axis] for bd in bds], ()), ) +
              seq[0].chunks[axis + 1:])

    cum_dims = [0] + list(accumulate(add, [len(a.chunks[axis]) for a in seq]))

    seq_dtypes = [a.dtype for a in seq]
    if len(set(seq_dtypes)) > 1:
        dt = reduce(np.promote_types, seq_dtypes)
        seq = [x.astype(dt) for x in seq]
    else:
        dt = seq_dtypes[0]

    names = [a.name for a in seq]

    name = 'concatenate-' + tokenize(names, axis)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))

    values = [(names[bisect(cum_dims, key[axis + 1]) - 1],) + key[1:axis + 1] +
              (key[axis + 1] - cum_dims[bisect(cum_dims, key[axis + 1]) - 1], ) +
              key[axis + 2:] for key in keys]

    dsk = dict(zip(keys, values))
    dsk2 = sharedict.merge((name, dsk), * [a.dask for a in seq])

    return Array(dsk2, name, chunks, dtype=dt)
