def _dequantize_per_channel_int8(
    x_i8, scales, zero_points, ch_axis, quant_min, quant_max
):
    # the following will be replaced as placeholders
    out_fp32 = torch.ops.quantized_decomposed.dequantize_per_channel(
        x_i8, scales, zero_points, ch_axis, quant_min, quant_max, torch.int8
    )
    return out_fp32
