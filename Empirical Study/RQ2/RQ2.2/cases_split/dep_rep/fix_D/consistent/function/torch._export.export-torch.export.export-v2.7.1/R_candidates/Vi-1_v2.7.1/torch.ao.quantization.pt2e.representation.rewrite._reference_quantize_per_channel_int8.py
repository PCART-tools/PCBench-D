def _reference_quantize_per_channel_int8(
    x_fp32, scales, zero_points, ch_axis, quant_min, quant_max
):
    x_fp32 = torch.transpose(x_fp32, ch_axis, -1)
    out_i32 = torch.ops.aten.clamp(
        torch.round(x_fp32 / scales).to(torch.int32) + zero_points, quant_min, quant_max
    )
    out_i32 = torch.transpose(out_i32, ch_axis, -1)
    return out_i32.to(torch.int8)
