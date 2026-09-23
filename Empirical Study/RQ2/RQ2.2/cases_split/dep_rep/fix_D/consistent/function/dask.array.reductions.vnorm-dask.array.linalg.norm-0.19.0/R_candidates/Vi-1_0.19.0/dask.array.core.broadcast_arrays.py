@wraps(np.broadcast_arrays)
def broadcast_arrays(*args, **kwargs):
    subok = bool(kwargs.pop("subok", False))

    to_array = asanyarray if subok else asarray
    args = tuple(to_array(e) for e in args)

    if kwargs:
        raise TypeError("unsupported keyword argument(s) provided")

    shape = broadcast_shapes(*(e.shape for e in args))
    chunks = broadcast_chunks(*(e.chunks for e in args))

    result = [broadcast_to(e, shape=shape, chunks=chunks) for e in args]

    return result
