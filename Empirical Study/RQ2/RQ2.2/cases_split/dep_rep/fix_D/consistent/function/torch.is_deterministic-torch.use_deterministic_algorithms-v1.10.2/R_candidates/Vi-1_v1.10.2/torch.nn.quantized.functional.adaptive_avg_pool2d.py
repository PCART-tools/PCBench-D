def adaptive_avg_pool2d(input: Tensor, output_size: BroadcastingList2[int]) -> Tensor:
    r"""
    Applies a 2D adaptive average pooling over a quantized input signal composed
    of several quantized input planes.

    .. note:: The input quantization parameters propagate to the output.

    See :class:`~torch.nn.quantized.AdaptiveAvgPool2d` for details and output shape.

    Args:
        output_size: the target output size (single integer or
                     double-integer tuple)
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.functional.adaptive_avg_pool2d' must be quantized!")
    return torch.nn.functional.adaptive_avg_pool2d(input, output_size)
