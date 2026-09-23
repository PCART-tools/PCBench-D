def _fake_quantize_per_tensor_affine_reference(X, scale, zero_point, quant_min, quant_max):
    dtype = X.dtype
    res = ((torch.clamp(torch.round(X.to(torch.float32) * (1.0 / scale) + zero_point), quant_min, quant_max) - zero_point) * scale)
    return res.to(dtype)
