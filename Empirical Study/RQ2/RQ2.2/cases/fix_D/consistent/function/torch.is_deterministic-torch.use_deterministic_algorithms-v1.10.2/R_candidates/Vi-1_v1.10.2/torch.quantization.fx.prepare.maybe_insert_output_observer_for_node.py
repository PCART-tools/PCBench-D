def maybe_insert_output_observer_for_node(
    node: Node,
    model: torch.nn.Module,
    modules: Dict[str, torch.nn.Module],
    graph: Graph,
    matches: Dict[str, MatchResult],
    node_name_to_target_dtype: Dict[str, Any],
    matched_pattern: Any,
    qhandler: Optional[QuantizeHandler],
) -> Optional[Node]:
    """
    If `node` needs an output observer, creates it, inserts it into `graph`
    and returns it.

    If `node` does not need an output observer, returns None.
    """
    root_node, matched_nodes, pattern, qhandler, qconfig = matches.get(
        node.name, (None, None, None, None, None))

    if qhandler is None:
        return None

    assert qconfig is not None
    assert node.op != 'output', 'observer insertion for outputs is handled elsewhere'

    is_standalone_module = qhandler is not None and \
        isinstance(qhandler, StandaloneModuleQuantizeHandler)

    dtype = node_name_to_target_dtype[node.name]
    should_insert_observer = \
        qhandler.should_insert_observer_for_output(
            qconfig, model.training) and dtype not in (torch.bool, None, torch.float)
    # TODO(future PR): move the following logic to
    # should_insert_observer_for_output
    should_insert_observer = should_insert_observer and \
        activation_is_statically_quantized(qconfig)

    # we never insert observers to output of standalone module, we assume
    # if needed, they are inserted inside the standalone module
    should_insert_observer = should_insert_observer and \
        (not is_standalone_module)

    if should_insert_observer:
        act_post_process_ctr = qconfig.activation
        if activation_is_int8_quantized(qconfig):
            act_post_process_ctr = \
                get_default_output_activation_post_process_map().get(
                    matched_pattern,
                    act_post_process_ctr)
        observer = act_post_process_ctr()
        new_obs = insert_observer(node, observer, model, modules, graph)
        # set the type, so the next node can read it
        node_name_to_target_dtype[new_obs.name] = \
            node_name_to_target_dtype[node.name]
        return new_obs
    else:
        return None
