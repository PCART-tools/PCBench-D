def _get_getitem_users(node: torch.fx.Node) -> set[torch.fx.Node]:
    node_users = list(node.users.keys())
    getitem_users = set()
    for user in node_users:
        if user.op == "output":
            continue

        assert user.op == "call_function" and user.target == operator.getitem, (
            f"Expected getitem node as user for {node}, instead got {user}"
        )
        getitem_users.update(list(user.users.keys()))
    return getitem_users
