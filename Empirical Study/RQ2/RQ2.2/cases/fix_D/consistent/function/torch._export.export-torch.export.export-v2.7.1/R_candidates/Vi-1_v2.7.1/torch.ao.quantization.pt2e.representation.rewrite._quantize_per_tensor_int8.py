def _quantize_per_tensor_int8(x_fp32, scale, zero_point, quant_min, quant_max):
    x = torch.ops.quantized_decomposed.quantize_per_tensor(
        x_fp32, scale, zero_point, quant_min, quant_max, torch.int8
    )
    return x
