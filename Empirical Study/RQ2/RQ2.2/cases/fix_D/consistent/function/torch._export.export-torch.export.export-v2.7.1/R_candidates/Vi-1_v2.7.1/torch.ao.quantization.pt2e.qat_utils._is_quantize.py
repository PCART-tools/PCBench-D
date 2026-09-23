def _is_quantize(n: Node) -> bool:
    return n.target in [
        torch.ops.quantized_decomposed.quantize_per_tensor.default,
        torch.ops.quantized_decomposed.quantize_per_tensor.tensor,
        torch.ops.quantized_decomposed.quantize_per_channel.default,
    ]
