def assign_memory_planning_info_for_scheduler_nodes(
    nodes: list[BaseSchedulerNode],
    name_to_fused_node: dict[str, BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer],
) -> None:
    """
    Assign to each scheduler node its predecessor and successor nodes.
    """
    from .scheduler import SchedulerBuffer

    for index, node in enumerate(nodes):
        size_alloc = sum(buffer.mpi_buffer.size_alloc for buffer in node.get_outputs())
        pred_buffers = OrderedSet[Union[SchedulerBuffer, FreeableInputBuffer]]()
        for dep in node.read_writes.reads:
            if dep.name in name_to_buf and dep in node.unmet_dependencies:
                pred_buffers.add(name_to_buf[dep.name])
            elif dep.name in name_to_freeable_input_buf:
                pred_buffers.add(name_to_freeable_input_buf[dep.name])
        pred_nodes = OrderedSet(
            name_to_fused_node[pred_buffer.defining_op_name()]
            for pred_buffer in pred_buffers
            if (isinstance(pred_buffer, SchedulerBuffer))
        )
        succ_nodes = OrderedSet(
            succ_node
            for buffer in node.get_outputs()
            for succ_node in buffer.mpi_buffer.succ_nodes
        )
        node.mpi_node = MemoryPlanningInfoForNode(
            index=index,
            size=size_alloc,
            pred_buffers=pred_buffers,
            pred_nodes=pred_nodes,
            succ_nodes=succ_nodes,
        )
