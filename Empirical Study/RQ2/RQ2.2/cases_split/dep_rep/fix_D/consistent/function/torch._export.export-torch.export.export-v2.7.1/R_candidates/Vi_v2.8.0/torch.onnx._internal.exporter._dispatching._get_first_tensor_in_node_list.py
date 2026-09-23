def _get_first_tensor_in_node_list(
    nodes: Sequence[torch.fx.Node | Any],
) -> torch.Tensor | None:
    for node in nodes:
        if (
            isinstance(node, torch.fx.Node)
            and "val" in node.meta
            and isinstance(node.meta["val"], torch.Tensor)
        ):
            return node.meta["val"]
    return None
