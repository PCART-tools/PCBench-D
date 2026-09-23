def topk(a, k, axis=-1, split_every=None):
    """ Extract the k largest elements from a on the given axis,
    and return them sorted from largest to smallest.
    If k is negative, extract the -k smallest elements instead,
    and return them sorted from smallest to largest.

    This performs best when ``k`` is much smaller than the chunk size. All
    results will be returned in a single chunk along the given axis.

    Parameters
    ----------
    x: Array
        Data being sorted
    k: int
    axis: int, optional
    split_every: int >=2, optional
        See :func:`reduce`. This parameter becomes very important when k is
        on the same order of magnitude of the chunk size or more, as it
        prevents getting the whole or a significant portion of the input array
        in memory all at once, with a negative impact on network transfer
        too when running on distributed.

    Returns
    -------
    Selection of x with size abs(k) along the given axis.

    Examples
    --------
    >>> import dask.array as da
    >>> x = np.array([5, 1, 3, 6])
    >>> d = da.from_array(x, chunks=2)
    >>> d.topk(2).compute()
    array([6, 5])
    >>> d.topk(-2).compute()
    array([1, 3])
    """
    axis = validate_axis(axis, a.ndim)

    # chunk and combine steps of the reduction, which recursively invoke
    # np.partition to pick the top/bottom k elements from the previous step.
    # The selection is not sorted internally.
    chunk_combine = partial(chunk.topk, k=k)
    # aggregate step of the reduction. Internally invokes the chunk/combine
    # function, then sorts the results internally.
    aggregate = partial(chunk.topk_aggregate, k=k)

    return reduction(
        a, chunk=chunk_combine, combine=chunk_combine, aggregate=aggregate,
        axis=axis, keepdims=True, dtype=a.dtype, split_every=split_every,
        output_size=abs(k))
