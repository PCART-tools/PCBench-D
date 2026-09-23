def _fake_quantize_learnable_per_channel_affine_grad_reference(
        dY, X, per_channel_scale, per_channel_zero_point, axis, quant_min, quant_max, device):
    r"""This method references the following literatures for back propagation on scale and zero point.
    - https://arxiv.org/pdf/1902.08153.pdf
    - https://arxiv.org/pdf/1903.08066.pdf
    """
    per_channel_zero_point = ((per_channel_zero_point.detach() + 0.5).clamp(quant_min, quant_max)).type(torch.int32)
    grad_X = _fake_quantize_per_channel_affine_grad_reference(
        dY, X, per_channel_scale, per_channel_zero_point, axis, quant_min, quant_max).to(device)
    per_channel_scale = per_channel_scale.detach().type(torch.float)

    grad_scale = torch.zeros([per_channel_scale.size(0)]).to(device)
    grad_zero_point = torch.zeros([per_channel_zero_point.size(0)]).to(device)

    X_flattened = torch.unbind(X, dim=axis)
    dY_flattened = torch.unbind(dY, dim=axis)

    for i, X_i in enumerate(torch.unbind(X, dim=axis), 0):
        scale_i = per_channel_scale[i]
        zero_point_i = per_channel_zero_point[i]
        X_i = X_flattened[i]
        dY_i = dY_flattened[i]

        Xq_i = ((X_i / scale_i) + zero_point_i).round()
        Xfq_i = (Xq_i - zero_point_i) * scale_i

        indicate_small_scale_i = (Xq_i < quant_min).float().to(device)
        indicate_big_scale_i = (Xq_i > quant_max).float().to(device)
        indicate_middle_scale_i = torch.ones(indicate_small_scale_i.shape).to(device) - \
            indicate_small_scale_i - indicate_big_scale_i

        indicate_saturate_zp_i = ((Xq_i < quant_min).float() +
                                  (Xq_i > quant_max).float()).to(device)
        indicate_unsaturate_zp_i = torch.ones(indicate_saturate_zp_i.shape).to(device) - \
            indicate_saturate_zp_i

        Xq_i = Xq_i.clamp(quant_min, quant_max)
        Xfq_i = (Xq_i - zero_point_i) * scale_i

        grad_small_scale_i = quant_min - zero_point_i
        grad_big_scale_i = quant_max - zero_point_i
        grad_middle_scale_i = ((Xfq_i - X_i) / scale_i).to(device)

        grad_saturate_zp_i = -scale_i.to(device)
        grad_unsaturate_zp_i = 0

        grad_scale_i = indicate_small_scale_i * grad_small_scale_i + \
            indicate_middle_scale_i * grad_middle_scale_i + \
            indicate_big_scale_i * grad_big_scale_i
        grad_zp_i = indicate_saturate_zp_i * grad_saturate_zp_i + \
            indicate_unsaturate_zp_i * grad_unsaturate_zp_i

        grad_scale_i = (grad_scale_i * dY_i).sum().unsqueeze(dim=0)
        grad_zp_i = (grad_zp_i * dY_i).sum().unsqueeze(dim=0)

        grad_scale[i] = grad_scale_i
        grad_zero_point[i] = grad_zp_i
    return grad_X, grad_scale, grad_zero_point
