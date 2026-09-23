def hardtanh_replacement(x, scale, zero_point):
    x = torch.nn.functional.hardtanh(x)
    return x
