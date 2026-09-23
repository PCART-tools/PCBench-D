def lp_pool2d(
    input: Tensor, norm_type: float,
    kernel_size: int,
    stride: Optional[BroadcastingList2[int]] = None,
    ceil_mode: bool = False
) -> Tensor:
    r"""Applies a 2D power-average pooling over an input signal composed of
    several input planes. If the sum of all inputs to the power of `p` is
    zero, the gradient is set to zero as well.

    See :class:`~torch.nn.LPPool2d` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            lp_pool2d, (input,), input, norm_type, kernel_size, stride=stride, ceil_mode=ceil_mode
        )
    kw, kh = utils._pair(kernel_size)
    if stride is not None:
        out = avg_pool2d(input.pow(norm_type), kernel_size, stride, 0, ceil_mode)
    else:
        out = avg_pool2d(input.pow(norm_type), kernel_size, padding=0, ceil_mode=ceil_mode)

    return (torch.sign(out) * relu(torch.abs(out))).mul(kw * kh).pow(1.0 / norm_type)
