def prepare_for_propagation_comparison(model: GraphModule) -> GraphModule:
    """Add output loggers to node that has numeric_debug_handle

    Args:
        model (GraphModule): original model
    Returns:
        a model with output loggers for all nodes that has numeric_debug_handle_id
    """
    # don't change the original model
    model = copy.deepcopy(model)
    for n in model.graph.nodes:
        if (
            CUSTOM_KEY not in n.meta
            or NUMERIC_DEBUG_HANDLE_KEY not in n.meta[CUSTOM_KEY]
        ):
            continue
        numeric_debug_handle = n.meta[CUSTOM_KEY][NUMERIC_DEBUG_HANDLE_KEY]
        _insert_logger(model, n, numeric_debug_handle)

    model.recompile()
    return model
