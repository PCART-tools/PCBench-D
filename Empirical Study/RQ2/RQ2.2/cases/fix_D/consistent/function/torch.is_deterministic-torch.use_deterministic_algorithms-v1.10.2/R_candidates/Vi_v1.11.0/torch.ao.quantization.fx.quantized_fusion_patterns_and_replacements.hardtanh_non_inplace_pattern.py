def hardtanh_non_inplace_pattern(x, scale, zero_point):
    x = x.dequantize()
    x = torch.nn.functional.hardtanh(x, inplace=False)
    x = torch.quantize_per_tensor(x, scale, zero_point, torch.quint8)
    return x
