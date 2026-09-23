def _quantize_weight(
        weight: torch.Tensor,
        weight_qscheme: torch.qscheme,
        weight_dtype: torch.dtype,
        weight_scale: torch.Tensor,
        weight_zero_point: torch.Tensor,
        weight_axis: torch.Tensor):
    if weight_qscheme == torch.per_tensor_affine:
        weight = torch.quantize_per_tensor(weight, weight_scale, weight_zero_point, weight_dtype)
    elif weight_qscheme in [torch.per_channel_affine, torch.per_channel_affine_float_qparams]:
        weight = torch.quantize_per_channel(
            weight, weight_scale,
            weight_zero_point, weight_axis.item(), weight_dtype)  # type: ignore[arg-type]
    else:
        raise Exception(f"Unsupported qscheme: {weight_qscheme}")
    return weight
