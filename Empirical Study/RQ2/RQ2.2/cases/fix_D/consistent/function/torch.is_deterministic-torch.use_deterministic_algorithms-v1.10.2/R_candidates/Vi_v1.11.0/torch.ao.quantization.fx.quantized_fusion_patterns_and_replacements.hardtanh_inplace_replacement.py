def hardtanh_inplace_replacement(x, scale, zero_point):
    x = torch.nn.functional.hardtanh_(x)
    return x
