def _maybe_insert_input_and_output_observers_for_node(
    node: Node,
    model: torch.fx.GraphModule,
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
):
    this_node_quantization_annotation = (
        node.meta["quantization_annotation"]
        if "quantization_annotation" in node.meta
        else None
    )
    if this_node_quantization_annotation is None:
        return

    named_modules = dict(model.named_modules(remove_duplicate=False))
    _maybe_insert_input_observers_for_node(
        node,
        None,  # qconfig
        model,
        named_modules,
        obs_or_fq_map,
        is_qat,
    )

    output_is_a_tensor = "val" in node.meta and isinstance(node.meta["val"], FakeTensor)
    if not output_is_a_tensor:
        return

    # this returns the new observer node if it was needed
    maybe_output_obs_node = _maybe_insert_output_observer_for_node(
        node, model, named_modules, model.graph, obs_or_fq_map, is_qat
    )

    if maybe_output_obs_node is None:
        return
    # Update users of original node to use the output observer
    # instead. For example, change
    #
    #           next_node
    #          /
    #   cur_node -> obs
    #
    # to
    #
    #                 next_node
    #                 /
    #   cur_node -> obs
    #
    # We need to save orig users before updating uses because
    # the list of users will change as we update uses
    orig_users = list(node.users.keys())
    for user_node in orig_users:
        if user_node is maybe_output_obs_node:
            continue
        user_node.replace_input_with(node, maybe_output_obs_node)
