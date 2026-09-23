def _maybe_insert_output_observer_for_node(
    node: Node,
    model: torch.nn.Module,
    named_modules: dict[str, torch.nn.Module],
    graph: Graph,
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
) -> Optional[Node]:
    if node in obs_or_fq_map:
        output_act_obs_or_fq = obs_or_fq_map[node]
        new_output = _insert_obs_or_fq(
            node, output_act_obs_or_fq, model, named_modules, graph
        )
        # propagate numeric debug handle from original node to observer/fake_quant node
        if (
            isinstance(node, Node)
            and isinstance(new_output, Node)
            and CUSTOM_KEY in node.meta
            and NUMERIC_DEBUG_HANDLE_KEY in node.meta[CUSTOM_KEY]
        ):
            if CUSTOM_KEY not in new_output.meta:
                new_output.meta[CUSTOM_KEY] = {}
            new_output.meta[CUSTOM_KEY][NUMERIC_DEBUG_HANDLE_KEY] = node.meta[
                CUSTOM_KEY
            ][NUMERIC_DEBUG_HANDLE_KEY]
        return new_output
    return None
