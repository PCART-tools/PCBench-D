@impl(quantized_decomposed_lib, "quantize_per_tensor.tensor", "Meta")
def quantize_per_tensor_tensor_meta(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
) -> torch.Tensor:
    if input.dtype in [torch.float16, torch.bfloat16]:
        input = input.to(torch.float32)
    assert (
        zero_point.numel() == 1
    ), f"Expecting zero_point tensor to be one element, but received : {zero_point.numel()}"
    assert (
        scale.numel() == 1
    ), f"Expecting scale tensor to be one element, but received : {scale.numel()}"
    assert (
        input.dtype == torch.float32
    ), f"Expecting input to have dtype torch.float32, but got dtype: {input.dtype}"
    return torch.empty_like(input, dtype=dtype)
