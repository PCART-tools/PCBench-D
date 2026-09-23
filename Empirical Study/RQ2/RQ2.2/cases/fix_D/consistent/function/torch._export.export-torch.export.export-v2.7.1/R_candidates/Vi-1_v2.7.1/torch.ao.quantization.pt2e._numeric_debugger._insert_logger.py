def _insert_logger(model: GraphModule, node: Node, debug_handle: int) -> Node:
    """For a given node, adds an OutputLogger that observes the output of that node,
    and all its users use the OutputLogger output instead.
    The OutputLogger will contain the debug_handle which can be used to compare
    graphs after transforms"""

    # to avoid circular dep
    from torch.ao.quantization.fx.utils import get_new_attr_name_with_prefix

    # add a logger after the node
    with model.graph.inserting_after(node):
        get_new_attr_name = get_new_attr_name_with_prefix(f"{node.name}_logger")
        logger_name = get_new_attr_name(model)
        setattr(
            model,
            logger_name,
            OutputLogger(debug_handle, node.name, node.meta.get("nn_module_stack")),
        )
        logger_node = model.graph.call_module(logger_name, (node,), {})

    orig_users = list(node.users.keys())
    for user_node in orig_users:
        if user_node is logger_node:
            continue
        user_node.replace_input_with(node, logger_node)

    return logger_node
