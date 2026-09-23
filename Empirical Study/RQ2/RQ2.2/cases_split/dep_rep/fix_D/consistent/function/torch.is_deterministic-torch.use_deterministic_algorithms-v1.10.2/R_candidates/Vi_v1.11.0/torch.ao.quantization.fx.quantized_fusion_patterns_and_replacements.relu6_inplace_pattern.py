def relu6_inplace_pattern(x, scale, zero_point):
    x = x.dequantize()
    x = torch.nn.functional.relu6(x, inplace=True)
    x = torch.quantize_per_tensor(x, scale, zero_point, torch.quint8)
    return x
