@wraps(np.insert)
def insert(arr, obj, values, axis):
    # axis is a required argument here to avoid needing to deal with the numpy
    # default case (which reshapes the array to make it flat)
    axis = validate_axis(axis,arr.ndim)

    if isinstance(obj, slice):
        obj = np.arange(*obj.indices(arr.shape[axis]))
    obj = np.asarray(obj)
    scalar_obj = obj.ndim == 0
    if scalar_obj:
        obj = np.atleast_1d(obj)

    obj = np.where(obj < 0, obj + arr.shape[axis], obj)
    if (np.diff(obj) < 0).any():
        raise NotImplementedError(
            'da.insert only implemented for monotonic ``obj`` argument')

    split_arr = split_at_breaks(arr, np.unique(obj), axis)

    if getattr(values, 'ndim', 0) == 0:
        # we need to turn values into a dask array
        name = 'values-' + tokenize(values)
        dtype = getattr(values, 'dtype', type(values))
        values = Array({(name,): values}, name, chunks=(), dtype=dtype)

        values_shape = tuple(len(obj) if axis == n else s
                             for n, s in enumerate(arr.shape))
        values = broadcast_to(values, values_shape)
    elif scalar_obj:
        values = values[(slice(None),) * axis + (None,)]

    values_chunks = tuple(values_bd if axis == n else arr_bd
                          for n, (arr_bd, values_bd)
                          in enumerate(zip(arr.chunks,
                                           values.chunks)))
    values = values.rechunk(values_chunks)

    counts = np.bincount(obj)[:-1]
    values_breaks = np.cumsum(counts[counts > 0])
    split_values = split_at_breaks(values, values_breaks, axis)

    interleaved = list(interleave([split_arr, split_values]))
    interleaved = [i for i in interleaved if i.nbytes]
    return concatenate(interleaved, axis=axis)
