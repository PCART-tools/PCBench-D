def _is_conv_node(n: Node):
    """
    Return whether the node refers to an aten conv op.
    """
    return n.op == "call_function" and n.target in [
        torch.ops.aten.conv1d.default,
        torch.ops.aten.conv2d.default,
    ]
