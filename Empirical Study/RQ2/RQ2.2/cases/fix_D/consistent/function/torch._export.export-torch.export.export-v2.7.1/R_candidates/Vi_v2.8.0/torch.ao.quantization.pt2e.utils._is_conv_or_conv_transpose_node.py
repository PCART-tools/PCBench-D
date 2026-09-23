def _is_conv_or_conv_transpose_node(n: Node):
    """
    Return whether the node refers to an aten conv or conv transpose op.
    """
    return _is_conv_node(n) or _is_conv_transpose_node(n)
