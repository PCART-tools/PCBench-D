def load_store_chunk(x, out, index, lock, return_stored, load_stored):
    """
    A function inserted in a Dask graph for storing a chunk.

    Parameters
    ----------
    x: array-like
        An array (potentially a NumPy one)
    out: array-like
        Where to store results too.
    index: slice-like
        Where to store result from ``x`` in ``out``.
    lock: Lock-like or False
        Lock to use before writing to ``out``.
    return_stored: bool
        Whether to return ``out``.
    load_stored: bool
        Whether to return the array stored in ``out``.
        Ignored if ``return_stored`` is not ``True``.

    Examples
    --------

    >>> a = np.ones((5, 6))
    >>> b = np.empty(a.shape)
    >>> load_store_chunk(a, b, (slice(None), slice(None)), False, False, False)
    """

    result = None
    if return_stored and not load_stored:
        result = out

    if lock:
        lock.acquire()
    try:
        if x is not None:
            out[index] = np.asanyarray(x)
        if return_stored and load_stored:
            result = out[index]
    finally:
        if lock:
            lock.release()

    return result
