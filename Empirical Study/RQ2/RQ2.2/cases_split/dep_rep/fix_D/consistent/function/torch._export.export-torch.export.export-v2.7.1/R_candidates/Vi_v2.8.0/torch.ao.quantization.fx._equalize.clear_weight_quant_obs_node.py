def clear_weight_quant_obs_node(op_node: Node, modules: dict[str, nn.Module]) -> None:
    """Given the operation node, we want find the corresponding quantization
    observer and reset its min/max values
    """
    weight_eq_obs_node = maybe_get_weight_eq_obs_node(op_node, modules)
    if weight_eq_obs_node is None:
        return

    weight_quant_obs_node = weight_eq_obs_node.args[0]
    if weight_quant_obs_node is None:
        return
    assert isinstance(weight_quant_obs_node, Node)

    weight_quant_obs = modules[str(weight_quant_obs_node.target)]
    assert isinstance(modules[str(weight_quant_obs_node.target)], ObserverBase)
    weight_quant_obs.reset_min_max_vals()  # type: ignore[operator]
