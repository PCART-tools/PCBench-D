def reorder_for_peak_memory(
    nodes: list[BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
    name_to_fused_node: dict[str, BaseSchedulerNode],
    graph_inputs: OrderedSet[str],
    graph_outputs: OrderedSet[str],
    methods: list[Callable[..., list[BaseSchedulerNode]]] = [  # noqa: B006
        topological_sort_lpmf,
        topological_sort_bfs,
        topological_sort_dfs,
    ],
) -> list[BaseSchedulerNode]:
    """
    Try a few heuristics based topological sort algorithms, and pick the one whose
    resulting topological order has the lowest peak memory estimation.
    """

    torch_log.info("Reordering for peak memory -- %d nodes", len(nodes))

    estimated_peak_memory, name_to_freeable_input_buf = prepare_planning_info(
        nodes,
        name_to_buf,
        name_to_fused_node,
        graph_inputs,
        graph_outputs,
    )

    # keep track of the peak memory estimates of different methods
    peak_memory_diff_methods: list[PeakMemoryResult] = []
    peak_memory_diff_methods.append(
        PeakMemoryResult(nodes, estimated_peak_memory, "baseline")
    )
    torch_log.info("Baseline peak memory: %d", estimated_peak_memory)

    # other methods
    for method in methods:
        try:
            if method == topological_sort_lpmf:
                order = method(
                    nodes, name_to_freeable_input_buf, name_to_buf, graph_outputs
                )
            else:
                order = method(nodes)
            assert len(order) == len(nodes)
            peak_memory, _ = estimate_peak_memory(
                order, name_to_freeable_input_buf, graph_outputs
            )
            peak_memory_diff_methods.append(
                PeakMemoryResult(order, peak_memory, method.__name__)
            )
            torch_log.info("%s peak memory: %d", method.__name__, peak_memory)
        except Exception as e:
            torch_log.error("Failed to reorder for %s: %s", method.__name__, e)

    signpost_event(
        category="inductor",
        name="memory",
        parameters={
            "orm": {elem.method: elem.peak_memory for elem in peak_memory_diff_methods},
        },
    )

    # get the optimal one
    best_result = min(peak_memory_diff_methods, key=lambda x: x.peak_memory)

    return best_result.order
