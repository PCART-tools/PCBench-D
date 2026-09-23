@impl(quantized_decomposed_lib, "quantize_per_tensor.tensor2", "Meta")
def quantize_per_tensor_tensor2_meta(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: torch.Tensor,
    quant_max: torch.Tensor,
    dtype: torch.dtype,
) -> torch.Tensor:
    return quantize_per_tensor_tensor_meta(
        input, scale, zero_point, quant_min, quant_max, dtype  # type: ignore[arg-type]
    )
