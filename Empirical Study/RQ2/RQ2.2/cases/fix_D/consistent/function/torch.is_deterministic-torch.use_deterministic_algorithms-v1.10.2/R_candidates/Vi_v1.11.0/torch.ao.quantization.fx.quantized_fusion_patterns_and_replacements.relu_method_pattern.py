def relu_method_pattern(x, scale, zero_point):
    x = x.dequantize()
    x = x.relu()
    x = torch.quantize_per_tensor(x, scale, zero_point, torch.quint8)
    return x
