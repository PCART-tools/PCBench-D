def _unique_internal(ar, indices, counts, return_inverse=False):
    """
    Helper/wrapper function for :func:`numpy.unique`.

    Uses :func:`numpy.unique` to find the unique values for the array chunk.
    Given this chunk may not represent the whole array, also take the
    ``indices`` and ``counts`` that are in 1-to-1 correspondence to ``ar``
    and reduce them in the same fashion as ``ar`` is reduced. Namely sum
    any counts that correspond to the same value and take the smallest
    index that corresponds to the same value.

    To handle the inverse mapping from the unique values to the original
    array, simply return a NumPy array created with ``arange`` with enough
    values to correspond 1-to-1 to the unique values. While there is more
    work needed to be done to create the full inverse mapping for the
    original array, this provides enough information to generate the
    inverse mapping in Dask.

    Given Dask likes to have one array returned from functions like
    ``atop``, some formatting is done to stuff all of the resulting arrays
    into one big NumPy structured array. Dask is then able to handle this
    object and can split it apart into the separate results on the Dask
    side, which then can be passed back to this function in concatenated
    chunks for further reduction or can be return to the user to perform
    other forms of analysis.

    By handling the problem in this way, it does not matter where a chunk
    is in a larger array or how big it is. The chunk can still be computed
    on the same way. Also it does not matter if the chunk is the result of
    other chunks being run through this function multiple times. The end
    result will still be just as accurate using this strategy.
    """

    return_index = (indices is not None)
    return_counts = (counts is not None)

    u = np.unique(ar)

    dt = [("values", u.dtype)]
    if return_index:
        dt.append(("indices", np.intp))
    if return_inverse:
        dt.append(("inverse", np.intp))
    if return_counts:
        dt.append(("counts", np.intp))

    r = np.empty(u.shape, dtype=dt)
    r["values"] = u
    if return_inverse:
        r["inverse"] = np.arange(len(r), dtype=np.intp)
    if return_index or return_counts:
        for i, v in enumerate(r["values"]):
            m = (ar == v)
            if return_index:
                indices[m].min(keepdims=True, out=r["indices"][i:i + 1])
            if return_counts:
                counts[m].sum(keepdims=True, out=r["counts"][i:i + 1])

    return r
