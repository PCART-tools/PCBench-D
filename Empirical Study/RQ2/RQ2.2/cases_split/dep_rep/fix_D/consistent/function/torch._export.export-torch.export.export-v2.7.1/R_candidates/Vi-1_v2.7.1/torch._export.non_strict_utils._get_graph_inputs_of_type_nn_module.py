def _get_graph_inputs_of_type_nn_module(
    args: Optional[tuple[tuple[Any], dict[Any, Any]]],
) -> set[type[torch.nn.Module]]:
    if args is None:
        return set()
    module_types = set()
    for arg in pytree.tree_leaves(args):
        if isinstance(arg, torch.nn.Module):
            module_types.add(type(arg))
    return module_types
