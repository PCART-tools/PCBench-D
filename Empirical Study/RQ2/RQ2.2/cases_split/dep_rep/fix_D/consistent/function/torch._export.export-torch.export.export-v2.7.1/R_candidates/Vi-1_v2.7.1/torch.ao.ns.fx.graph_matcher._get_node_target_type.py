def _get_node_target_type(node: Node, gm: GraphModule) -> Optional[NSNodeTargetType]:
    if node.op in ("call_function", "call_method"):
        return node.target
    elif node.op == "call_module":
        assert isinstance(node.target, str)
        mod = getattr_from_fqn(gm, node.target)
        return type(mod)
    return None
