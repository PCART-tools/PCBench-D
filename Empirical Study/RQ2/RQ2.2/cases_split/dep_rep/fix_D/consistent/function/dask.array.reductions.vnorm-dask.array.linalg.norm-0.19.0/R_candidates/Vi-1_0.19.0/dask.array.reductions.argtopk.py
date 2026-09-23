def argtopk(a, k, axis=-1, split_every=None):
    """ Extract the indices of the k largest elements from a on the given axis,
    and return them sorted from largest to smallest. If k is negative, extract
    the indices of the -k smallest elements instead, and return them sorted
    from smallest to largest.

    This performs best when ``k`` is much smaller than the chunk size. All
    results will be returned in a single chunk along the given axis.

    Parameters
    ----------
    x: Array
        Data being sorted
    k: int
    axis: int, optional
    split_every: int >=2, optional
        See :func:`topk`. The performance considerations for topk also apply
        here.

    Returns
    -------
    Selection of np.intp indices of x with size abs(k) along the given axis.

    Examples
    --------
    >>> import dask.array as da
    >>> x = np.array([5, 1, 3, 6])
    >>> d = da.from_array(x, chunks=2)
    >>> d.argtopk(2).compute()
    array([3, 0])
    >>> d.argtopk(-2).compute()
    array([1, 2])
    """
    axis = validate_axis(axis, a.ndim)

    # Generate nodes where every chunk is a tuple of (a, original index of a)
    idx = arange(a.shape[axis], chunks=(a.chunks[axis], ), dtype=np.intp)
    idx = idx[tuple(slice(None) if i == axis else np.newaxis
                    for i in range(a.ndim))]
    a_plus_idx = a.map_blocks(chunk.argtopk_preprocess, idx,
                              dtype=object)

    # chunk and combine steps of the reduction. They acquire in input a tuple
    # of (a, original indices of a) and return another tuple containing the top
    # k elements of a and the matching original indices. The selection is not
    # sorted internally, as in np.argpartition.
    chunk_combine = partial(chunk.argtopk, k=k)
    # aggregate step of the reduction. Internally invokes the chunk/combine
    # function, then sorts the results internally, drops a and returns the
    # index only.
    aggregate = partial(chunk.argtopk_aggregate, k=k)

    return reduction(
        a_plus_idx, chunk=chunk_combine, combine=chunk_combine,
        aggregate=aggregate, axis=axis, keepdims=True, dtype=np.intp,
        split_every=split_every, concatenate=False, output_size=abs(k))
