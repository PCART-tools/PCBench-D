def stack(seq, axis=0):
    """
    Stack arrays along a new axis

    Given a sequence of dask arrays, form a new dask array by stacking them
    along a new dimension (axis=0 by default)

    Examples
    --------

    Create slices

    >>> import dask.array as da
    >>> import numpy as np

    >>> data = [from_array(np.ones((4, 4)), chunks=(2, 2))
    ...          for i in range(3)]

    >>> x = da.stack(data, axis=0)
    >>> x.shape
    (3, 4, 4)

    >>> da.stack(data, axis=1).shape
    (4, 3, 4)

    >>> da.stack(data, axis=-1).shape
    (4, 4, 3)

    Result is a new dask Array

    See Also
    --------
    concatenate
    """
    n = len(seq)
    ndim = len(seq[0].shape)
    if axis < 0:
        axis = ndim + axis + 1
    if axis > ndim:
        raise ValueError("Axis must not be greater than number of dimensions"
                         "\nData has %d dimensions, but got axis=%d" %
                         (ndim, axis))
    if not all(x.shape == seq[0].shape for x in seq):
        idx = np.where(np.asanyarray([x.shape for x in seq]) != seq[0].shape)[0]
        raise ValueError("Stacked arrays must have the same shape. "
                         "The first {0} had shape {1}, while array "
                         "{2} has shape {3}".format(idx[0],
                                                    seq[0].shape,
                                                    idx[0] + 1,
                                                    seq[idx[0]].shape))

    ind = list(range(ndim))
    uc_args = list(concat((x, ind) for x in seq))
    _, seq = unify_chunks(*uc_args)

    dt = reduce(np.promote_types, [a.dtype for a in seq])
    seq = [x.astype(dt) for x in seq]

    assert len(set(a.chunks for a in seq)) == 1  # same chunks
    chunks = (seq[0].chunks[:axis] + ((1,) * n,) + seq[0].chunks[axis:])

    names = [a.name for a in seq]
    name = 'stack-' + tokenize(names, axis)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))

    inputs = [(names[key[axis + 1]], ) + key[1:axis + 1] + key[axis + 2:]
              for key in keys]
    values = [(getitem, inp, (slice(None, None, None),) * axis +
              (None, ) + (slice(None, None, None), ) * (ndim - axis))
              for inp in inputs]

    dsk = dict(zip(keys, values))
    dsk2 = sharedict.merge((name, dsk), *[a.dask for a in seq])

    return Array(dsk2, name, chunks, dtype=dt)
