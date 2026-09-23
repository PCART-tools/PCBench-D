def _fake_quantize_learnable_per_tensor_affine_grad_reference(dY, X, scale, zero_point, quant_min, quant_max, device):
    r"""This method references the following literatures for back propagation on scale and zero point.
    - https://arxiv.org/pdf/1902.08153.pdf
    - https://arxiv.org/pdf/1903.08066.pdf
    """
    zero_point_rounded = int((zero_point + 0.5).clamp(quant_min, quant_max).item())
    Xq = torch.round(X * (1.0 / scale) + zero_point_rounded)

    indicate_small_scale = (Xq < quant_min).float().to(device)
    indicate_big_scale = (Xq > quant_max).float().to(device)
    indicate_middle_scale = torch.ones(indicate_small_scale.shape).to(device) - \
        indicate_small_scale - indicate_big_scale

    indicate_saturate_zp = ((Xq < quant_min).float() + (Xq > quant_max).float()).to(device)
    indicate_unsaturate_zp = torch.ones(indicate_saturate_zp.shape).to(device) - indicate_saturate_zp

    Xq = Xq.clamp(quant_min, quant_max)
    Xfq = (Xq - zero_point_rounded) * scale

    grad_small_scale = quant_min - zero_point_rounded
    grad_big_scale = quant_max - zero_point_rounded
    grad_middle_scale = ((Xfq - X) / scale).to(device)

    grad_saturate_zp = -scale.to(device)
    grad_unsaturate_zp = 0

    grad_scale = indicate_small_scale * grad_small_scale + \
        indicate_big_scale * grad_big_scale + \
        indicate_middle_scale * grad_middle_scale
    grad_zp = indicate_saturate_zp * grad_saturate_zp + \
        indicate_unsaturate_zp * grad_unsaturate_zp
    grad_X = _fake_quantize_per_tensor_affine_grad_reference(
        dY, X, scale, zero_point, quant_min, quant_max).to(device)

    grad_scale = (grad_scale * dY).sum().unsqueeze(dim=0)
    grad_zp = (grad_zp * dY).sum().unsqueeze(dim=0)
    return grad_X, grad_scale, grad_zp
