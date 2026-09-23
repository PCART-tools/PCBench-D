def _quantize_per_channel_int8(
    x_fp32, scales, zero_points, ch_axis, quant_min, quant_max
):
    out_i8 = torch.ops.quantized_decomposed.quantize_per_channel(
        x_fp32, scales, zero_points, ch_axis, quant_min, quant_max, torch.int8
    )
    return out_i8
