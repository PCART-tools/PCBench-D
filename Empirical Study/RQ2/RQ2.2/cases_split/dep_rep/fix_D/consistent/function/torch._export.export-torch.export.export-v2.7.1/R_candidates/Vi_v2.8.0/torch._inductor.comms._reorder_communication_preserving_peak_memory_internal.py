def _reorder_communication_preserving_peak_memory_internal(
    snodes: list[BaseSchedulerNode],
) -> tuple[list[BaseSchedulerNode], dict[BaseSchedulerNode, ReorderInfo]]:
    """
    Internal testing helper that also returns debug info.
    Returns:
        - reordered snodes list
        - dict {snode: ReorderInfo}
    """
    # heuristic to avoid degenerating to quadratic time
    MOVE_LIMIT = len(snodes) * 100
    total_moves = 0
    # TODO - experiment with whether this limit is useful, setting `len(snodes)` disables it
    PER_COLLECTIVE_PREFETCH_LIMIT = len(snodes)
    if config.reorder_prefetch_limit is not None:
        PER_COLLECTIVE_PREFETCH_LIMIT = config.reorder_prefetch_limit
    graph_inputs: OrderedSet[str] = OrderedSet(V.graph.graph_inputs.keys())
    graph_outputs: OrderedSet[str] = OrderedSet(V.graph.get_output_names())
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer] = get_freeable_input_buf(
        snodes, graph_inputs
    )
    peak_memory, curr_memory = estimate_peak_memory(
        snodes, name_to_freeable_input_buf, graph_outputs
    )
    runtimes = {snode: estimate_op_runtime(snode) for snode in snodes}

    # debug stats
    stats: dict[BaseSchedulerNode, ReorderInfo] = {}

    def exposed_communication_time(collective_snode, remaining_snodes):
        # assumes a linear schedule and computes the overlap of the collective with the remaining nodes
        comm_time = estimate_op_runtime(collective_snode)
        compute_time = 0.0
        for snode in remaining_snodes:
            if contains_collective(snode):
                continue
            if contains_wait(snode):
                # TODO - if the wait is for a collective that started before this collective or on another stream,
                # we can ignore it. Otherwise, it's the end of the road for overlap opportunities
                break

            compute_time += runtimes[snode]
        return max(0, comm_time - compute_time)

    for i, snode in enumerate(snodes):
        if contains_collective(snode):
            reorder_info = stats[snode] = ReorderInfo()
            reorder_info.initial_exposed = reorder_info.final_exposed = (
                exposed_communication_time(snode, snodes[i + 1 :])
            )
            if total_moves >= MOVE_LIMIT:
                reorder_info.limiting_factor = "move limit"
                continue
            for j in range(i - 1, -1, -1):
                prev_snode = snodes[j]
                if j < max(0, i - PER_COLLECTIVE_PREFETCH_LIMIT):
                    reorder_info.limiting_factor = "prefetch limit"
                    break
                if contains_collective(prev_snode):
                    reorder_info.limiting_factor = "collective ordering"
                    break
                dep_names = OrderedSet([s.name for s in snode.unmet_dependencies])
                if any(
                    o.get_name() in dep_names for o in prev_snode.get_outputs()
                ) and not contains_wait(prev_snode):
                    reorder_info.limiting_factor = "data dependency"
                    break
                if peak_memory - curr_memory[j] < curr_memory[j - 1] - curr_memory[j]:
                    reorder_info.limiting_factor = "peak memory"
                    break
                if reorder_info.final_exposed > runtimes[snode]:
                    reorder_info.limiting_factor = "sufficient overlapping"
                    break
                reorder_info.moves += 1
                total_moves += 1
                tmp = snodes[j]
                snodes[j] = snodes[j + 1]
                snodes[j + 1] = tmp
                # swapping nodes j and j+1 affects curr memory at j only
                j_plus_one_alloc = curr_memory[j + 1] - curr_memory[j]
                j_alloc = curr_memory[j] - curr_memory[j - 1]
                curr_memory[j] = curr_memory[j] - j_alloc + j_plus_one_alloc
                reorder_info.final_exposed = exposed_communication_time(
                    snode, snodes[j + 1 :]
                )

    return snodes, stats
