def quantize_APoT(
    tensor2quantize: Tensor,
    alpha: Tensor,
    gamma: Tensor,
    quantization_levels: Tensor,
    level_indices: Tensor,
):
    quantizer = APoTQuantizer(
        alpha=alpha,
        gamma=gamma,
        quantization_levels=quantization_levels,
        level_indices=level_indices,
    )
    result = quantizer.quantize(tensor2quantize)
    return result
