def get_aten_target(node: fx.Node) -> Callable:
    if hasattr(node.target, "overloadpacket"):
        return node.target.overloadpacket
    return node.target
