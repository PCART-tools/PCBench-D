def max_pool2d(
    input,
    kernel_size,
    stride=None,
    padding=0,
    dilation=1,
    ceil_mode=False,
    return_indices=False,
):
    r"""Applies a 2D max pooling over a quantized input signal composed of
    several quantized input planes.

    .. note:: The input quantization parameters are propagated to the output.

    See :class:`~torch.ao.nn.quantized.MaxPool2d` for details.
    """
    if return_indices:
        raise NotImplementedError("return_indices is not yet implemented!")
    if stride is None:
        stride = torch.jit.annotate(list[int], [])
    return torch.nn.functional.max_pool2d(
        input,
        kernel_size,
        stride,
        padding,
        dilation,
        ceil_mode=ceil_mode,
        return_indices=return_indices,
    )
