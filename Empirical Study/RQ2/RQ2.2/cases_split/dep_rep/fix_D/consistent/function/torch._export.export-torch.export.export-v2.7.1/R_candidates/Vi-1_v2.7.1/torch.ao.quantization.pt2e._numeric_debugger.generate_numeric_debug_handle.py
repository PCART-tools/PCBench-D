def generate_numeric_debug_handle(ep: ExportedProgram) -> None:
    """
    Attach numeric_debug_handle_id for all nodes in the graph module of the given
    ExportedProgram, like conv2d, squeeze, conv1d, etc, except for placeholder.
    Notice that nodes like getattr are out of scope since they are not in the graph.

    The graph nodes of input exported program are modified inplace.

    Here's an example of using debug handle quantize flow::

        ep = export_for_training(eager_model, example_inputs)
        generate_numeric_debug_handle(ep)

        m = ep.module()
        quantizer = XNNPACKQuantizer()
        m = prepare_pt2e(m, quantizer)
        m = convert_pt2e(m)
    """

    # Sanity check the input data type
    if not isinstance(ep, ExportedProgram):
        raise ValueError(
            f"Expected ep to be ExportedProgram, got {type(ExportedProgram)}"
        )

    unique_id = 0

    def _find_max_id(node: torch.fx.Node) -> None:
        nonlocal unique_id
        unique_id = max(
            unique_id, node.meta.get(CUSTOM_KEY, {}).get(NUMERIC_DEBUG_HANDLE_KEY, 0)
        )

    def _assign_debug_handle(node: torch.fx.Node) -> None:
        nonlocal unique_id
        if CUSTOM_KEY not in node.meta:
            node.meta[CUSTOM_KEY] = {}

        if NUMERIC_DEBUG_HANDLE_KEY not in node.meta[CUSTOM_KEY]:
            node.meta[CUSTOM_KEY][NUMERIC_DEBUG_HANDLE_KEY] = unique_id
            unique_id += 1

    # Find the max ID that exists in the graph first, in case part of the graph
    # has already been annotated. This way we guarantee there are no duplicate
    # handle IDs.
    bfs_trace_with_node_process(ep, _find_max_id)

    unique_id += 1

    # Assign debug handles to all nodes in the graph that don't have one based on the
    # max ID found in the previous step.
    bfs_trace_with_node_process(ep, _assign_debug_handle)
