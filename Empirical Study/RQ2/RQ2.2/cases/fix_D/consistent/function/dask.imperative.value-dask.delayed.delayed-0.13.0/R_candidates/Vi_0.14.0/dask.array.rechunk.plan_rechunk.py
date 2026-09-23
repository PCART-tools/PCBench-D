def plan_rechunk(old_chunks, new_chunks, itemsize,
                 threshold=DEFAULT_THRESHOLD,
                 block_size_limit=DEFAULT_BLOCK_SIZE_LIMIT):
    """ Plan an iterative rechunking from *old_chunks* to *new_chunks*.
    The plan aims to minimize the rechunk graph size.

    Parameters
    ----------
    itemsize: int
        The item size of the array
    threshold: int
        The graph growth factor under which we don't bother
        introducing an intermediate step
    block_size_limit: int
        The maximum block size (in bytes) we want to produce during an
        intermediate step
    """
    ndim = len(new_chunks)
    steps = []
    if ndim <= 1 or not all(new_chunks):
        # Trivial array => no need for an intermediate
        return steps + [new_chunks]

    # Make it a number ef elements
    block_size_limit /= itemsize

    # Fix block_size_limit if too small for either old_chunks or new_chunks
    largest_old_block = _largest_block_size(old_chunks)
    largest_new_block = _largest_block_size(new_chunks)
    block_size_limit = max([block_size_limit,
                            largest_old_block,
                            largest_new_block,
                            ])

    # The graph size above which to optimize
    graph_size_threshold = threshold * (_number_of_blocks(old_chunks) +
                                        _number_of_blocks(new_chunks))

    current_chunks = old_chunks
    first_pass = True

    while True:
        graph_size = estimate_graph_size(current_chunks, new_chunks)
        if graph_size < graph_size_threshold:
            break

        if first_pass:
            chunks = current_chunks
        else:
            # We hit the block_size_limit in a previous merge pass =>
            # accept a significant increase in graph size in exchange for
            # 1) getting nearer the goal 2) reducing the largest block size
            # to make place for the following merge.
            # To see this pass in action, make the block_size_limit very small.
            chunks = find_split_rechunk(current_chunks, new_chunks,
                                        graph_size * threshold)
        chunks, memory_limit_hit = find_merge_rechunk(chunks, new_chunks,
                                                      block_size_limit)
        if chunks == current_chunks or chunks == new_chunks:
            break
        steps.append(chunks)
        current_chunks = chunks
        if not memory_limit_hit:
            break
        first_pass = False

    return steps + [new_chunks]
