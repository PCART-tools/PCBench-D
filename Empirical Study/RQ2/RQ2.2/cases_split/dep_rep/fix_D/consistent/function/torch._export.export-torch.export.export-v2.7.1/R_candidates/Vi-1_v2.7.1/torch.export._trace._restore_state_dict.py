def _restore_state_dict(
    original_module: torch.nn.Module, traced_module: torch.fx.GraphModule
) -> None:
    """
    Restores the state dict of the traced module to that of the original module.
    """
    param_buffer_table = _get_param_buffer_mapping(original_module, traced_module)
    # Since the graph module is flattened (no module heirarchy), we
    # need to noramlize the module by replacing "." with "_". If we
    # don't, it will try to save the weight to a submodule which no
    # longer exists.
    for name, fqn in param_buffer_table.items():
        param_buffer_table[name] = fqn.replace(".", "_")

    # Replace state dict attr names with the fqn
    for name, fqn in param_buffer_table.items():
        if not hasattr(traced_module, name):
            continue

        attr = getattr(traced_module, name)
        if isinstance(attr, torch.Tensor) and not isinstance(attr, torch.nn.Parameter):
            traced_module.register_buffer(fqn, attr)
        else:
            setattr(traced_module, fqn, attr)
        delattr(traced_module, name)

    # Replace graph getattr nodes with the correct name
    for node in traced_module.graph.nodes:
        if node.op == "get_attr":
            attr_name = node.target
            if attr_name in param_buffer_table:
                node.target = param_buffer_table[attr_name]

    traced_module.recompile()
