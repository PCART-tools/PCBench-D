def _get_external_inputs(
    region: Region,
) -> dict[Node, tuple[int, int]]:
    external_node_to_indices = dict()
    region_unique = set(region)
    for node_ind, node in enumerate(region):
        flattened_args_kwargs = _flatten_args_kwargs((node.args, node.kwargs))
        for arg_ind, in_node in enumerate(flattened_args_kwargs):
            if (
                isinstance(in_node, Node)
                and in_node not in region_unique
                and in_node not in external_node_to_indices
            ):
                external_node_to_indices[in_node] = (node_ind, arg_ind)

    return external_node_to_indices
