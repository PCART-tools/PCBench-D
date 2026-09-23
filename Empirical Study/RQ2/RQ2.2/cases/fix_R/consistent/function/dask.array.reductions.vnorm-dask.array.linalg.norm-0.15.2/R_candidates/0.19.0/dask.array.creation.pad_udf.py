def pad_udf(array, pad_width, mode, **kwargs):
    """
    Helper function for padding boundaries with a user defined function.

    In cases where the padding requires a custom user defined function be
    applied to the array, this function assists in the prepping and
    application of this function to the Dask Array to construct the desired
    boundaries.
    """

    result = pad_edge(array, pad_width, "constant", 0)

    chunks = result.chunks
    for d in range(result.ndim):
        result = result.rechunk(
            chunks[:d] + (result.shape[d:d + 1],) + chunks[d + 1:]
        )

        result = result.map_blocks(
            wrapped_pad_func,
            token="pad",
            dtype=result.dtype,
            pad_func=mode,
            iaxis_pad_width=pad_width[d],
            iaxis=d,
            pad_func_kwargs=kwargs,
        )

        result = result.rechunk(chunks)

    return result
