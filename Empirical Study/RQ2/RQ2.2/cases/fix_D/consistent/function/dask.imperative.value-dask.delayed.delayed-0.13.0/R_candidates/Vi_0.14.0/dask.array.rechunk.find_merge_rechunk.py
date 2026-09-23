def find_merge_rechunk(old_chunks, new_chunks, block_size_limit):
    """
    Find an intermediate rechunk that would merge some adjacent blocks
    together in order to get us nearer the *new_chunks* target, without
    violating the *block_size_limit* (in number of elements).
    """
    ndim = len(old_chunks)

    old_largest_width = [max(c) for c in old_chunks]
    new_largest_width = [max(c) for c in new_chunks]

    graph_size_effect = {
        dim: len(nc) / len(oc)
        for dim, (oc, nc) in enumerate(zip(old_chunks, new_chunks))
    }

    block_size_effect = {
        dim: new_largest_width[dim] / old_largest_width[dim]
        for dim in range(ndim)
    }

    # Our goal is to reduce the number of nodes in the rechunk graph
    # by merging some adjacent chunks, so consider dimensions where we can
    # reduce the # of chunks
    merge_candidates = [dim for dim in range(ndim)
                        if graph_size_effect[dim] <= 1.0]

    # Merging along each dimension reduces the graph size by a certain factor
    # and increases memory largest block size by a certain factor.
    # We want to optimize the graph size while staying below the given
    # block_size_limit.  This is in effect a knapsack problem, except with
    # multiplicative values and weights.  Just use a greedy algorithm
    # by trying dimensions in decreasing value / weight order.
    def key(k):
        gse = graph_size_effect[k]
        bse = block_size_effect[k]
        if bse == 1:
            bse = 1 + 1e-9
        return np.log(gse) / np.log(bse)

    sorted_candidates = sorted(merge_candidates, key=key)

    largest_block_size = reduce(mul, old_largest_width)

    chunks = list(old_chunks)
    memory_limit_hit = False

    for dim in sorted_candidates:
        # Examine this dimension for possible graph reduction
        new_largest_block_size = (
            largest_block_size * new_largest_width[dim] // old_largest_width[dim])
        if new_largest_block_size <= block_size_limit:
            # Full replacement by new chunks is possible
            chunks[dim] = new_chunks[dim]
            largest_block_size = new_largest_block_size
        else:
            # Try a partial rechunk, dividing the new chunks into
            # smaller pieces
            largest_width = old_largest_width[dim]
            chunk_limit = int(block_size_limit * largest_width / largest_block_size)
            c = divide_to_width(new_chunks[dim], chunk_limit)
            if len(c) <= len(old_chunks[dim]):
                # We manage to reduce the number of blocks, so do it
                chunks[dim] = c
                largest_block_size = largest_block_size * max(c) // largest_width

            memory_limit_hit = True

    assert largest_block_size == _largest_block_size(chunks)
    assert largest_block_size <= block_size_limit
    return tuple(chunks), memory_limit_hit
