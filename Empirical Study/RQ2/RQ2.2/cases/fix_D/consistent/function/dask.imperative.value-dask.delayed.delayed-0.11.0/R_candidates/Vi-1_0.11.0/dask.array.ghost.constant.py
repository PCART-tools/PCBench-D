def constant(x, axis, depth, value):
    """ Add constant slice to either side of array """
    chunks = list(x.chunks)
    chunks[axis] = (depth,)

    c = wrap.full(tuple(map(sum, chunks)), value,
                  chunks=tuple(chunks), dtype=x._dtype)

    return concatenate([c, x, c], axis=axis)
