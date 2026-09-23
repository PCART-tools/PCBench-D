def add_dummy_padding(x, depth, boundary):
    """
    Pads an array which has 'none' as the boundary type.
    Used to simplify trimming arrays which use 'none'.

    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)
    >>> add_dummy_padding(x, {0: 1}, {0: 'none'}).compute()  # doctest: +NORMALIZE_WHITESPACE
    array([..., 0, 1, 2, 3, 4, 5, ...])
    """
    for k, v in boundary.items():
        d = depth.get(k, 0)
        if v == 'none' and d > 0:
            empty_shape = list(x.shape)
            empty_shape[k] = d

            empty_chunks = list(x.chunks)
            empty_chunks[k] = (d,)

            empty = wrap.empty(empty_shape, chunks=empty_chunks, dtype=x.dtype)

            out_chunks = list(x.chunks)
            ax_chunks = list(out_chunks[k])
            ax_chunks[0] += d
            ax_chunks[-1] += d
            out_chunks[k] = tuple(ax_chunks)

            x = concatenate([empty, x, empty], axis=k)
            x = x.rechunk(out_chunks)
    return x
