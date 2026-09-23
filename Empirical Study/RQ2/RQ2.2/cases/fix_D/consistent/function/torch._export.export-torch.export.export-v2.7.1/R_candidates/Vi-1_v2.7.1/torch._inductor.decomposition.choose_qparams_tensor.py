@register_decomposition(quantized_decomposed.choose_qparams.tensor)
def choose_qparams_tensor(
    input: torch.Tensor,
    quant_min: int,
    quant_max: int,
    eps: float,
    dtype: torch.dtype,
) -> tuple[torch.Tensor, torch.Tensor]:
    min_val, max_val = torch.aminmax(input)
    scale = (max_val - min_val) / float(quant_max - quant_min)
    scale = torch.max(scale, torch.Tensor([eps]))
    zero_point = quant_min - torch.round(min_val / scale).to(torch.int)
    zero_point = torch.clamp(zero_point, quant_min, quant_max)
    return scale.to(torch.float64), zero_point.to(torch.int64)
