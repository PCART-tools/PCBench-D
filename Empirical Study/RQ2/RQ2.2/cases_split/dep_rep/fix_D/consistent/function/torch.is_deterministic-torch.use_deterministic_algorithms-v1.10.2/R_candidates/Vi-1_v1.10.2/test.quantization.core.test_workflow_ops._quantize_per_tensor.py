def _quantize_per_tensor(x, scale, zero_point, quant_min, quant_max):
    return ((x / scale) + zero_point).round().clamp(quant_min, quant_max)
