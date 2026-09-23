def is_get_tensor_info_node(node: Node) -> bool:
    """ Returns True if this node is a node that takes a Tensor as input and output some
    meta information about the Tensor, e.g. shape, size etc.
    """
    result: bool = \
        node.op == "call_function" and node.target == getattr and node.args[1] == "shape"  # type: ignore[assignment]
    return result
