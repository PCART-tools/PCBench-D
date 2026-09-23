def _filter_sym_size_users(node: torch.fx.Node) -> list[torch.fx.Node]:
    node_users = list(filter((lambda x: (_is_sym_size_node(x) is False)), node.users))
    return node_users
