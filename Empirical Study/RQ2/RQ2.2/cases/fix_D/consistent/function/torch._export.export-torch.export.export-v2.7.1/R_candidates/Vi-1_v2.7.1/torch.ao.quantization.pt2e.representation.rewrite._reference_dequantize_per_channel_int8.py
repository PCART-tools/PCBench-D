def _reference_dequantize_per_channel_int8(
    x_i8, scales, zero_points, ch_axis, quant_min, quant_max
):
    # the following will be replaced as placeholders
    # in order to preserve the quant_min/quant_max args for pattern matching (e.g. matching for int4 quantized ops)
    # we call a torch.ops.aten.clamp here
    x_i8 = torch.ops.aten.clamp(x_i8, quant_min, quant_max)
    x_i8 = torch.transpose(x_i8, ch_axis, -1)
    x_i32 = x_i8.to(torch.int32)
    out_fp32 = (x_i32 - zero_points).to(torch.float) * scales
    out_fp32 = torch.transpose(out_fp32, ch_axis, -1)
    return out_fp32
