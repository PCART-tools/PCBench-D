def get_freeable_input_buf(
    nodes: list[BaseSchedulerNode],
    graph_inputs: OrderedSet[str],
) -> dict[str, FreeableInputBuffer]:
    """
    Create and keep track of all input buffers that can be freed during the program

    Returns:
        A dictionary containing all freeble input buffers, keyed by their names.
    """

    # this function is copied from torch/_inductor/scheduler.py
    # TODO: would be nice to remove the try/except block for both places
    def _dep_size_hint(dep: Dep) -> int:
        res = 0
        try:
            if not dep.has_unbacked_symbols():
                res = dep.numbytes_hint()
        except KeyError:
            # In at least one test (test/inductor/test_torchbind.py) we
            # create a StarDep that doesn't exist in the graph and calling
            # `has_unbacked_symbols()` throws an error.
            pass
        return res

    # get freeable input buffers' successor nodes and their sizes
    # note that different deps can have the same name, so we use name as keys
    dep_name_to_succ_nodes: dict[str, OrderedSet[BaseSchedulerNode]] = (
        collections.defaultdict(OrderedSet)
    )
    dep_name_to_size: dict[str, int] = dict()
    for node in nodes:
        for dep in node.read_writes.reads:
            if dep.name in graph_inputs and not dep.name.startswith(
                ("primals_", "arg")
            ):
                dep_name_to_succ_nodes[dep.name].add(node)
                dep_name_to_size[dep.name] = _dep_size_hint(dep)

    # create FreeableInputBuffer objects and add them to the returned dictionary
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer] = dict()
    for dep_name, succ_nodes in dep_name_to_succ_nodes.items():
        name_to_freeable_input_buf[dep_name] = FreeableInputBuffer(
            dep_name,
            MemoryPlanningInfoForBuffer(
                size_free=dep_name_to_size[dep_name], succ_nodes=succ_nodes
            ),
        )
    return name_to_freeable_input_buf
