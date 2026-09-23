def _dequantize_per_tensor_int8(x_i8, scale, zero_point, quant_min, quant_max):
    x_fp32 = torch.ops.quantized_decomposed.dequantize_per_tensor(
        x_i8, scale, zero_point, quant_min, quant_max, torch.int8
    )
    return x_fp32
