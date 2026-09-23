def _default_custom_combo_kernel_horizontal_partition(
    nodes: list[BaseSchedulerNode],
    triton_scheduling: SIMDScheduling,
    kernel_map: dict[BaseSchedulerNode, TritonKernel],
    node_info_map: dict[BaseSchedulerNode, tuple[Any, Any, Any, Any]],
) -> list[list[BaseSchedulerNode]]:
    """Horizontally partition the given list of nodes into a list of list of nodes where each sublist
    represents a partition. Nodes in different partitions are implemented in different combo kernels.
    Nodes in the same partition are likely to be implemented
    in the same combo kernel, but subject to subsequent restrictions like CUDA limits for number of args.

    Input arguments:
        nodes: a list of fused scheduler nodes to partition.
        triton_scheduling: TritonScheduling instance.
        kernel_map: a map from node to its kernel.
        node_info_map: a map from node to (node_schedule, tiled_groups, numel, rnumel).
    Output:
        a list of list of nodes with each sublist representing a partition.

    The default algorithm is to partition nodes based on the following rules:
        1) nodes with the same number of block dimensions are grouped together.
        2) large pointwise nodes (numels greater than LARGE_NUMELS) are separated from other nodes.
        3) large reduce nodes are separated from other nodes.
    """

    assert len(nodes) >= 1

    # first partition nodes based on number of block dimensions
    tilings = [node_info_map[n][1] for n in nodes]

    max_dims = max(len(t) for t in tilings)
    nodes_per_ndim: list[list[BaseSchedulerNode]] = []
    for i in range(2, max_dims + 1):
        group_per_dim = [n for n, t in zip(nodes, tilings) if len(t) == i]
        reduction = [
            n
            for n in group_per_dim
            if kernel_map[n].inside_reduction
            and not (kernel_map[n].persistent_reduction and kernel_map[n].no_x_dim)
        ]
        not_reduction = [n for n in group_per_dim if n not in reduction]
        # rnumel > 2048 usually has long execution time
        # BaseSchedulerNode.group[-1][-1] is rnumel for reduction nodes
        long_reduction = [
            n
            for n in reduction
            if V.graph.sizevars.size_hint(n.group[-1][-1]) > 2048  # type: ignore[arg-type]
        ]
        short_reduction = [n for n in reduction if n not in long_reduction]
        if long_reduction:
            log.warning(
                "ComboKernels: %d long reduction nodes are separated",
                len(long_reduction),
            )
        large_pointwise = [
            n
            for n in not_reduction
            if not kernel_map[n].inside_reduction
            and len(kernel_map[n].numels) == 2
            and V.graph.sizevars.size_hint(kernel_map[n].numels["x"]) > LARGE_NUMELS
        ]
        if large_pointwise:
            # TODO benchmark the performance when large pointwise nodes combining with others
            log.warning(
                "ComboKernels: %d large pointwise nodes are separated",
                len(large_pointwise),
            )
            not_reduction = [n for n in not_reduction if n not in large_pointwise]
            nodes_per_ndim.extend([node] for node in large_pointwise)

        nodes_per_ndim.extend(
            g for g in (not_reduction, short_reduction, long_reduction) if g
        )

    assert sum(len(p) for p in nodes_per_ndim) == len(nodes)
    return nodes_per_ndim
