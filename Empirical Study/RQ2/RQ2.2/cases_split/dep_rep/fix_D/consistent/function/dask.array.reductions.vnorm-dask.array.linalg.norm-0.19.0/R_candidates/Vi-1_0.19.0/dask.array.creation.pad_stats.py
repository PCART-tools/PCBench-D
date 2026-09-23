def pad_stats(array, pad_width, mode, *args):
    """
    Helper function for padding boundaries with statistics from the array.

    In cases where the padding requires computations of statistics from part
    or all of the array, this function helps compute those statistics as
    requested and then adds those statistics onto the boundaries of the array.
    """

    if mode == "median":
        raise NotImplementedError("`pad` does not support `mode` of `median`.")

    stat_length = expand_pad_width(array, args[0])

    result = np.empty(array.ndim * (3,), dtype=object)
    for idx in np.ndindex(result.shape):
        axes = []
        select = []
        pad_shape = []
        pad_chunks = []
        for d, (i, s, c, w, l) in enumerate(zip(
            idx, array.shape, array.chunks, pad_width, stat_length
        )):
            if i < 1:
                axes.append(d)
                select.append(slice(None, l[0], None))
                pad_shape.append(w[0])
                pad_chunks.append(w[0])
            elif i > 1:
                axes.append(d)
                select.append(slice(s - l[1], None, None))
                pad_shape.append(w[1])
                pad_chunks.append(w[1])
            else:
                select.append(slice(None))
                pad_shape.append(s)
                pad_chunks.append(c)

        axes = tuple(axes)
        select = tuple(select)
        pad_shape = tuple(pad_shape)
        pad_chunks = tuple(pad_chunks)

        result_idx = array[select]
        if mode == "maximum":
            result_idx = result_idx.max(axis=axes, keepdims=True)
        elif mode == "mean":
            result_idx = result_idx.mean(axis=axes, keepdims=True)
        elif mode == "minimum":
            result_idx = result_idx.min(axis=axes, keepdims=True)

        result_idx = broadcast_to(result_idx, pad_shape, chunks=pad_chunks)

        result[idx] = result_idx

    result = block(result.tolist())

    return result
