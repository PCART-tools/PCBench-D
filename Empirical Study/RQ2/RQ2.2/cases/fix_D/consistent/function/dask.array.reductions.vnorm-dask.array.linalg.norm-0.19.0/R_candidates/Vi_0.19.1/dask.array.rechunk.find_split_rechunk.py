def find_split_rechunk(old_chunks, new_chunks, graph_size_limit):
    """
    Find an intermediate rechunk that would split some chunks to
    get us nearer *new_chunks*, without violating the *graph_size_limit*.
    """
    ndim = len(old_chunks)

    chunks = list(old_chunks)

    for dim in range(ndim):
        graph_size = estimate_graph_size(chunks, new_chunks)
        if graph_size > graph_size_limit:
            break
        if len(old_chunks[dim]) > len(new_chunks[dim]):
            # It's not interesting to split
            continue
        # Merge the new chunks so as to stay within the graph size budget
        max_number = int(len(old_chunks[dim]) * graph_size_limit / graph_size)
        c = merge_to_number(new_chunks[dim], max_number)
        assert len(c) <= max_number
        # Consider the merge successful if its result has a greater length
        # and smaller max width than the old chunks
        if len(c) >= len(old_chunks[dim]) and max(c) <= max(old_chunks[dim]):
            chunks[dim] = c

    return tuple(chunks)
