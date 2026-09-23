def _is_dequantize(n: Node) -> bool:
    return n.target in [
        torch.ops.quantized_decomposed.dequantize_per_tensor.default,
        torch.ops.quantized_decomposed.dequantize_per_tensor.tensor,
        torch.ops.quantized_decomposed.dequantize_per_channel.default,
    ]
