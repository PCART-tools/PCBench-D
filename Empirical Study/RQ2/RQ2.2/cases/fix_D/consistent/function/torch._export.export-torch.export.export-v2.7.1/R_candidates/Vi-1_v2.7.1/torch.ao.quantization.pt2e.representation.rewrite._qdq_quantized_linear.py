def _qdq_quantized_linear(
    x_i8,
    x_scale,
    x_zero_point,
    x_quant_min,
    x_quant_max,
    weight_i8,
    weight_scale,
    weight_zero_point,
    weight_quant_min,
    weight_quant_max,
    bias_fp32,
    out_scale,
    out_zero_point,
    out_quant_min,
    out_quant_max,
):
    x_fp32 = torch.ops.quantized_decomposed.dequantize_per_tensor(
        x_i8, x_scale, x_zero_point, x_quant_min, x_quant_max, torch.int8
    )
    weight_fp32 = torch.ops.quantized_decomposed.dequantize_per_tensor(
        weight_i8,
        weight_scale,
        weight_zero_point,
        weight_quant_min,
        weight_quant_max,
        torch.int8,
    )
    out_fp32 = torch.ops.aten.linear.default(x_fp32, weight_fp32, bias_fp32)
    out_i8 = torch.ops.quantized_decomposed.quantize_per_tensor(
        out_fp32, out_scale, out_zero_point, out_quant_min, out_quant_max, torch.int8
    )
    return out_i8
