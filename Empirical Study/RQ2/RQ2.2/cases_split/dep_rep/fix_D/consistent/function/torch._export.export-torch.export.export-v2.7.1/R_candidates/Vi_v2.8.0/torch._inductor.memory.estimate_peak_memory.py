def estimate_peak_memory(
    nodes: list[BaseSchedulerNode],
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer],
    graph_outputs: OrderedSet[str],
) -> tuple[int, list[int]]:
    """
    Given a list of nodes in their execution order, estimate the peak memory, by
    keeping track of the liveliness of SchedulerBuffers and FreeableInputBuffers.

    Returns:
        int: peak memory
        List[int]: memory usage at each node (or each step).
    """

    # map each scheduler buffer to its size, start step, and end step
    @dataclasses.dataclass
    class BufferInfo:
        buffer: Union[SchedulerBuffer, FreeableInputBuffer]
        size_alloc: int
        size_free: int
        start_step: int
        end_step: int

    # get the execution step of each node, this will be used to determine
    # the end_step of buffers
    node_to_step: dict[BaseSchedulerNode, int] = {
        node: step for step, node in enumerate(nodes)
    }

    # get buffers' size and liveliness information
    buf_info_list: list[BufferInfo] = []
    # 1. for freeable input buffers
    for buf_name, input_buf in name_to_freeable_input_buf.items():
        end_step = (
            len(nodes) - 1
            if buf_name in graph_outputs
            else max(
                node_to_step[succ_node] for succ_node in input_buf.mpi_buffer.succ_nodes
            )
        )
        buf_info_list.append(
            BufferInfo(
                input_buf,
                input_buf.mpi_buffer.size_free,
                input_buf.mpi_buffer.size_free,
                0,
                end_step,
            )
        )

    # 2. for scheduler buffers
    for step, node in enumerate(nodes):
        for sched_buf in node.get_outputs():
            # note: it is possible for a non-graph-output sched_buf to have no succ_nodes and
            # to be only used by its defining op (e.g., due to fusion when all consumers of
            # the buffer are fused with its defining op). In such cases, end_step is step.
            end_step = (
                len(nodes) - 1
                if sched_buf.get_name() in graph_outputs
                else max(
                    [
                        node_to_step[succ_node]
                        for succ_node in sched_buf.mpi_buffer.succ_nodes
                    ],
                    default=step,
                )
            )
            buf_info_list.append(
                BufferInfo(
                    sched_buf,
                    sched_buf.mpi_buffer.size_alloc,
                    sched_buf.mpi_buffer.size_free,
                    step,
                    end_step,
                )
            )

    # incremental memory changes at each step
    memory = [0 for _ in range(len(nodes) + 1)]

    # for each buffer, update memory when created and when freed
    for buf_info in buf_info_list:
        memory[buf_info.start_step] += buf_info.size_alloc
        memory[buf_info.end_step + 1] -= buf_info.size_free

    # get peak memory by compute the cumulative memories
    max_memory = 0
    cur_memory = 0
    memories_at_nodes = []
    for t in range(len(nodes) + 1):
        cur_memory += memory[t]
        memories_at_nodes.append(cur_memory)
        max_memory = max(max_memory, cur_memory)

    return (max_memory, memories_at_nodes)
