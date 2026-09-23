@impl(quantized_decomposed_lib, "dequantize_per_tensor.tensor2", "Meta")
def dequantize_per_tensor_tensor2_meta(
    input,
    scale,
    zero_point,
    quant_min,
    quant_max,
    dtype,
    *,
    out_dtype: Optional[torch.dtype] = None,
) -> torch.Tensor:
    return dequantize_per_tensor_tensor_meta(
        input, scale, zero_point, quant_min, quant_max, dtype, out_dtype=out_dtype
    )
