def topk(k, x):
    """ The top k elements of an array

    Returns the k greatest elements of the array in sorted order.  Only works
    on arrays of a single dimension.

    This assumes that ``k`` is small.  All results will be returned in a single
    chunk.

    Examples
    --------

    >>> x = np.array([5, 1, 3, 6])
    >>> d = from_array(x, chunks=2)
    >>> d.topk(2).compute()
    array([6, 5])
    """
    if x.ndim != 1:
        raise ValueError("Topk only works on arrays of one dimension")

    token = tokenize(k, x)
    name = 'chunk.topk-' + token
    dsk = dict(((name, i), (chunk.topk, k, key))
                for i, key in enumerate(x._keys()))
    name2 = 'topk-' + token
    dsk[(name2, 0)] = (getitem, (np.sort, (np.concatenate, (list, list(dsk)))),
                       slice(-1, -k - 1, -1))
    chunks = ((k,),)

    return Array(merge(dsk, x.dask), name2, chunks, dtype=x.dtype)
