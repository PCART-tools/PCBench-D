def _get_node_name_to_scope(model: GraphModule) -> dict[str, tuple[str, type]]:
    # TODO: move this information to fx node itself
    node_name_to_scope: dict[str, tuple[str, type]] = {}
    for n in model.graph.nodes:
        nn_module_stack = n.meta.get("nn_module_stack", None)
        current_scope = ("", type(None))
        if nn_module_stack:
            bt = list(nn_module_stack.values())[-1]
            current_scope = (bt[0].split(".")[-1], bt[1])
        node_name_to_scope[n.name] = current_scope
    return node_name_to_scope
