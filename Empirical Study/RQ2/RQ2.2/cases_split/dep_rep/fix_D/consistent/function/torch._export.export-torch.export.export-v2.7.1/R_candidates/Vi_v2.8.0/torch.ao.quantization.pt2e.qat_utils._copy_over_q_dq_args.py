def _copy_over_q_dq_args(original_node: Node, replacement_node: Node):
    """
    Given a pair of quantize or dequantize nodes, copy over all literal args
    from the original node to the replacement node.
    """
    # For quantize_per_tensor, scale and zp are literals and need to be copied
    # For quantize_per_channel, scale and zp are get_attr nodes and should be skipped
    assert original_node.target == replacement_node.target
    if original_node.target in (
        torch.ops.quantized_decomposed.quantize_per_tensor.default,
        torch.ops.quantized_decomposed.dequantize_per_tensor.default,
    ):
        # Args: input, [scale, zp, qmin, qmax, dtype]
        start_copy_arg_index = 1
    elif original_node.target in (
        torch.ops.quantized_decomposed.quantize_per_channel.default,
        torch.ops.quantized_decomposed.dequantize_per_channel.default,
    ):
        # Args: input, scale, zp, [axis, qmin, qmax, dtype]
        start_copy_arg_index = 3
    else:
        raise ValueError(
            f"Expected quantize/dequantize nodes, got '{original_node.target}'"
        )
    replacement_node.args = (
        replacement_node.args[:start_copy_arg_index]
        + original_node.args[start_copy_arg_index:]
    )
