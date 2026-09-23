def _is_tangent(node: fx.Node) -> bool:
    return node.op == "placeholder" and "tangents" in str(node.target)
