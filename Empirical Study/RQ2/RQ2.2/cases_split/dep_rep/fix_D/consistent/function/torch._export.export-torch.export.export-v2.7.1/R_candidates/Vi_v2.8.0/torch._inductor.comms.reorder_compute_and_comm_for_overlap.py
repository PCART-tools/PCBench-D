def reorder_compute_and_comm_for_overlap(
    snodes: list[BaseSchedulerNode],
) -> list[BaseSchedulerNode]:
    order = snodes
    graph_inputs: OrderedSet[str] = OrderedSet(V.graph.graph_inputs.keys())
    graph_outputs: OrderedSet[str] = OrderedSet(V.graph.get_output_names())
    for p in config.reorder_for_compute_comm_overlap_passes:
        if isinstance(p, str) and p in globals():
            p = globals()[p]  # it is a builtin pass
        assert callable(p), (
            f"Invalid reorder_compute_and_comm_for_overlap pass: {p} is not callable"
        )
        peak_memory, _ = estimate_peak_memory(
            snodes, get_freeable_input_buf(snodes, graph_inputs), graph_outputs
        )
        if torch.distributed.get_rank() == 0:
            overlap_log.debug(
                f"==== Visualize overlap before reordering pass {p}, {peak_memory=} ===="  # noqa: G004
            )
            try:
                visualize_overlap(order)
            except Exception as e:
                overlap_log.debug("", exc_info=e)
        t0 = time.time()
        order = p(order)  # type: ignore[operator]
        t = time.time() - t0
        if torch.distributed.get_rank() == 0:
            overlap_log.debug(
                f"==== Visualize overlap after reordering pass {p} (ran in {t} sec)===="  # noqa: G004
            )
            try:
                visualize_overlap(order)
            except Exception as e:
                overlap_log.debug("", exc_info=e)
        peak_memory, _ = estimate_peak_memory(
            snodes, get_freeable_input_buf(snodes, graph_inputs), graph_outputs
        )
        print(f"final {peak_memory=}")
    return order
