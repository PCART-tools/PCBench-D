def node_return_type_is_int(node: Node) -> bool:
    """
    Returns true if this node results in an integer, even if some of the args
    are Tensors.
    """
    return node.op == 'call_method' and node.target == 'size'
