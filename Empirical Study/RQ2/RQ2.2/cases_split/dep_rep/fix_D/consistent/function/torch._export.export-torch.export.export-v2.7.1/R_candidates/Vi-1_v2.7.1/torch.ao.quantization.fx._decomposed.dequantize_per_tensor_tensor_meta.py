@impl(quantized_decomposed_lib, "dequantize_per_tensor.tensor", "Meta")
def dequantize_per_tensor_tensor_meta(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: Optional[torch.dtype] = None,
) -> torch.Tensor:
    if out_dtype is None:
        out_dtype = torch.float32
    assert (
        zero_point.numel() == 1
    ), f"Expecting zero_point tensor to be one element, but received : {zero_point.numel()}"
    assert (
        scale.numel() == 1
    ), f"Expecting scale tensor to be one element, but received : {scale.numel()}"
    assert input.dtype == dtype, f"Expecting input to have dtype: {dtype}"
    if dtype in _DTYPE_TO_QVALUE_BOUNDS:
        return torch.empty_like(input, dtype=out_dtype)
    else:
        raise ValueError(f"Unsupported dtype in dequantize_per_tensor: {dtype}")
