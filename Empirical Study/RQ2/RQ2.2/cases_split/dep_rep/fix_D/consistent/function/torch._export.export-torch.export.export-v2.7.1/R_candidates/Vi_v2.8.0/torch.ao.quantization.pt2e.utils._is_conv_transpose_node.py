def _is_conv_transpose_node(n: Node):
    """
    Return whether the node refers to an aten conv_transpose op.
    """
    return n.op == "call_function" and n.target in [
        torch.ops.aten.conv_transpose1d,
        torch.ops.aten.conv_transpose1d.default,
        torch.ops.aten.conv_transpose2d,
        torch.ops.aten.conv_transpose2d.input,
    ]
