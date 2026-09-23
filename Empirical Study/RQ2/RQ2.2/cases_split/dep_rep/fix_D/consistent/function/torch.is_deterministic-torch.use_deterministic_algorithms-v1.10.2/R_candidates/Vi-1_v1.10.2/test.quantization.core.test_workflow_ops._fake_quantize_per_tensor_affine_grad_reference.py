def _fake_quantize_per_tensor_affine_grad_reference(dY, X, scale, zero_point, quant_min, quant_max):
    dtype = X.dtype
    Xq = torch.round(X.to(torch.float32) * (1.0 / scale) + zero_point)
    mask = (Xq >= quant_min) * (Xq <= quant_max)
    res = torch.zeros_like(dY)
    res[mask] = dY[mask]
    return res.to(dtype)
