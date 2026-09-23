def qpt(t, scale, zero_point, dtype=torch.quint8):
    t = torch.tensor(t)
    return torch.quantize_per_tensor(t, scale, zero_point, dtype)
