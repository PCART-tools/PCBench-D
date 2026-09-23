def is_node_meta_valid(node: Optional[torch.fx.Node]) -> bool:
    return node is None or "example_value" in node.meta or "val" in node.meta
