@impl(quantized_decomposed_lib, "choose_qparams.tensor", "Meta")
def choose_qparams_tensor_meta(
    input: torch.Tensor, quant_min: int, quant_max: int, eps: float, dtype: torch.dtype
) -> tuple[torch.Tensor, torch.Tensor]:
    assert input.dtype in [
        torch.float32,
        torch.float16,
        torch.bfloat16,
    ], f"Expecting input to have dtype torch.float32/16/b16, but got dtype: {input.dtype}"
    assert (
        quant_min < quant_max
    ), f"Expecting quant_min to be smaller than quant_max but received min: \
        {quant_min} max: {quant_max}"
    return torch.empty(1, dtype=torch.double, device=input.device), torch.empty(
        1, dtype=torch.int64, device=input.device
    )
