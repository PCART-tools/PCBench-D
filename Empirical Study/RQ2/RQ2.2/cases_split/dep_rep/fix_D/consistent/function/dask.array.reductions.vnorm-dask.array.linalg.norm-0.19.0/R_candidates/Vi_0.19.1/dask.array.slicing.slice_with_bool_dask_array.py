def slice_with_bool_dask_array(x, index):
    """ Slice x with one or more dask arrays of bools

    This is a helper function of `Array.__getitem__`.

    Parameters
    ----------
    x: Array
    index: tuple with as many elements as x.ndim, among which there are
           one or more Array's with dtype=bool

    Returns
    -------
    tuple of (sliced x, new index)

    where the new index is the same as the input, but with slice(None)
    replaced to the original slicer when a filter has been applied.

    Note: The sliced x will have nan chunks on the sliced axes.
    """
    from .core import Array, atop, elemwise

    out_index = [slice(None)
                 if isinstance(ind, Array) and ind.dtype == bool
                 else ind
                 for ind in index]

    if len(index) == 1 and index[0].ndim == x.ndim:
        y = elemwise(getitem, x, *index, dtype=x.dtype)
        name = 'getitem-' + tokenize(x, index)
        dsk = {(name, i): k for i, k in enumerate(core.flatten(y.__dask_keys__()))}
        chunks = ((np.nan,) * y.npartitions,)
        return (Array(sharedict.merge(y.dask, (name, dsk)), name, chunks, x.dtype),
                out_index)

    if any(isinstance(ind, Array) and ind.dtype == bool and ind.ndim != 1
           for ind in index):
        raise NotImplementedError("Slicing with dask.array of bools only permitted when "
                                  "the indexer has only one dimension or when "
                                  "it has the same dimension as the sliced "
                                  "array")
    indexes = [ind
               if isinstance(ind, Array) and ind.dtype == bool
               else slice(None)
               for ind in index]

    arginds = []
    i = 0
    for ind in indexes:
        if isinstance(ind, Array) and ind.dtype == bool:
            new = (ind, tuple(range(i, i + ind.ndim)))
            i += x.ndim
        else:
            new = (slice(None), None)
            i += 1
        arginds.append(new)

    arginds = list(concat(arginds))

    out = atop(getitem_variadic, tuple(range(x.ndim)), x, tuple(range(x.ndim)), *arginds, dtype=x.dtype)

    chunks = []
    for ind, chunk in zip(index, out.chunks):
        if isinstance(ind, Array) and ind.dtype == bool:
            chunks.append((np.nan,) * len(chunk))
        else:
            chunks.append(chunk)
    out._chunks = tuple(chunks)
    return out, tuple(out_index)
