def set_node_name(
    node: torch.fx.Node,
    new_name: str,
    name_to_node_cache: dict[str, torch.fx.Node],
):
    """Safely set the unique name of a node.

    If the new name is already taken by another node, the name of the other node will be
    updated. If `new_name` is a string of format f"{base_name}.{count}", where `count`
    is an integer, the other node will be renamed as f"{base_name}.{count+1}". If not,
    the other node will be renamed as "{new_name}.1". This function will iteratively
    update the names until there is no conflict.

    ``name_to_node_cache`` is required as an argument to avoid recomputation. The caller
    is responsible for ensuring the cache is accurate and in sync with the owning module
    of the node. The values in the cache will be updated accordingly.

    Args:
        node: The node to update.
        new_name: The new name to use.
        name_to_node_cache: A cache of node names to nodes.
    """
    node_name_to_set = collections.deque([(node, new_name)])

    while node_name_to_set:
        node, new_name = node_name_to_set.pop()
        if new_name in name_to_node_cache and name_to_node_cache[new_name] != node:
            base_name, postfix_count = _get_node_base_name(new_name)
            if postfix_count is None:
                postfix_count = 0
            node_name_to_set.append(
                (name_to_node_cache[new_name], f"{base_name}.{postfix_count + 1}")
            )
        node.name = new_name
        name_to_node_cache[new_name] = node
