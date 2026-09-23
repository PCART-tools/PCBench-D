def prepare(
    model: GraphModule,
    node_name_to_scope: dict[str, tuple[str, type]],
    is_qat: bool,
    obs_or_fq_callback=None,
) -> GraphModule:
    # Since we are mutating the graph as we go, we iterate over the original
    # nodes before observer insertion, instead of model.graph.nodes.
    nodes_before_observation = list(model.graph.nodes)

    # At the high level we construct a map from EdgeOrNode to a observer_or_fake_quant instance
    # all edge/nodes that belongs to the same group will use the same instance
    # and when we insert observers we'll just query this map to get the correct observer_or_fake_quant
    # instance
    edge_or_node_to_qspec = _get_edge_or_node_to_qspec(model)
    edge_or_node_to_group_id = _get_edge_or_node_to_group_id(edge_or_node_to_qspec)
    obs_or_fq_map = _get_obs_or_fq_map(
        edge_or_node_to_group_id, edge_or_node_to_qspec, is_qat
    )
    if obs_or_fq_callback:
        obs_or_fq_callback(model, obs_or_fq_map)

    for node in nodes_before_observation:
        # TODO: simplify logic for inserting observers
        _maybe_insert_input_and_output_observers_for_node(
            node, model, obs_or_fq_map, is_qat
        )

    model = GraphModule(model, model.graph)

    _save_state(
        model,
        {},  # node_name_to_qconfig
        node_name_to_scope,
        PrepareCustomConfig(),
        {},  # equalization_node_name_to_qconfig
        QConfigMapping(),
        is_qat,
        set(),  # observed_node_names
    )
    return model
