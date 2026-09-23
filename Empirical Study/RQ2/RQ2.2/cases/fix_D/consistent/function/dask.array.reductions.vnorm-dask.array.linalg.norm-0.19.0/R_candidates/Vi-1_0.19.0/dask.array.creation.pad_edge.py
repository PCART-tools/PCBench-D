def pad_edge(array, pad_width, mode, *args):
    """
    Helper function for padding edges.

    Handles the cases where the only the values on the edge are needed.
    """

    token = tokenize(array, pad_width, mode, args)
    name = 'pad-' + token
    numblocks = array.numblocks

    chunks = list()
    for d, c in enumerate(array.chunks):
        c = list(c)
        c[0] += pad_width[d][0]
        c[-1] += pad_width[d][-1]
        c = tuple(c)
        chunks.append(c)
    chunks = tuple(chunks)

    dsk = {}
    for idx in product(*(range(n) for n in numblocks)):
        pad_chunk_width = []
        for d, i in enumerate(idx):
            ith_pad_chunk_width = [0, 0]
            if i == 0:
                ith_pad_chunk_width[0] = pad_width[d][0]
            if i == numblocks[d] - 1:
                ith_pad_chunk_width[1] = pad_width[d][1]

            ith_pad_chunk_width = tuple(ith_pad_chunk_width)
            pad_chunk_width.append(ith_pad_chunk_width)

        pad_chunk_width = tuple(pad_chunk_width)

        array_chunk_key = (array.name,) + idx
        result_chunk_key = (name,) + idx

        if any(map(any, pad_chunk_width)):
            dsk[result_chunk_key] = (
                np_pad, array_chunk_key, pad_chunk_width, mode
            )
            dsk[result_chunk_key] += args
        else:
            dsk[result_chunk_key] = array_chunk_key

    dsk = sharedict.merge((name, dsk))
    dsk = sharedict.merge(dsk, array.dask)

    result = Array(dsk, name, chunks=chunks, dtype=array.dtype)

    return result
