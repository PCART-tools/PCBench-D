def slicing_plan(chunks, index):
    """ Construct a plan to slice chunks with the given index

    Parameters
    ----------
    chunks : Tuple[int]
        One dimensions worth of chunking information
    index : np.ndarray[int]
        The index passed to slice on that dimension

    Returns
    -------
    out : List[Tuple[int, np.ndarray]]
        A list of chunk/sub-index pairs corresponding to each output chunk
    """
    index = np.asanyarray(index)
    cum_chunks = np.cumsum(chunks)

    chunk_locations = np.searchsorted(cum_chunks, index, side='right')
    where = np.where(np.diff(chunk_locations))[0] + 1
    where = np.concatenate([[0], where, [len(chunk_locations)]])

    out = []
    for i in range(len(where) - 1):
        sub_index = index[where[i]:where[i + 1]]
        chunk = chunk_locations[where[i]]
        if chunk > 0:
            sub_index = sub_index - cum_chunks[chunk - 1]
        out.append((chunk, sub_index))

    return out
