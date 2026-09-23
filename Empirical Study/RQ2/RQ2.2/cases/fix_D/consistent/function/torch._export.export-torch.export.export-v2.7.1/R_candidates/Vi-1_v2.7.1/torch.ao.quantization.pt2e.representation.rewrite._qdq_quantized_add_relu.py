def _qdq_quantized_add_relu(
    x_i8,
    x_scale,
    x_zero_point,
    y_i8,
    y_scale,
    y_zero_point,
    out_scale,
    out_zero_point,
    quant_min,
    quant_max,
):
    x_fp32 = torch.ops.quantized_decomposed.dequantize_per_tensor(
        x_i8, x_scale, x_zero_point, quant_min, quant_max, torch.int8
    )
    y_fp32 = torch.ops.quantized_decomposed.dequantize_per_tensor(
        y_i8, y_scale, y_zero_point, quant_min, quant_max, torch.int8
    )
    out_fp32 = x_fp32 + y_fp32
    out_fp32 = torch.ops.aten.relu(out_fp32)
    out_i8 = torch.ops.quantized_decomposed.quantize_per_tensor(
        out_fp32, out_scale, out_zero_point, quant_min, quant_max, torch.int8
    )
    return out_i8
