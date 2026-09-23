def is_node_meta_valid(node: torch.fx.Node):
    return "val" in node.meta
