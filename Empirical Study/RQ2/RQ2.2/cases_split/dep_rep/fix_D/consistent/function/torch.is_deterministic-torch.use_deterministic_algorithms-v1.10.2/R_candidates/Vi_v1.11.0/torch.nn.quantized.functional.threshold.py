def threshold(input: Tensor, threshold: float, value: float) -> Tensor:
    r"""Applies the quantized version of the threshold function element-wise:

    .. math::
        x = \begin{cases}
                x & \text{if~} x > \text{threshold} \\
                \text{value} & \text{otherwise}
            \end{cases}

    See :class:`~torch.nn.Threshold` for more details.
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.threshold' must be quantized!")
    if threshold is None:
        raise ValueError("Input to 'threshold' must be specified!")
    if value is None:
        raise ValueError("Input to 'value' must be specified!")
    return torch._ops.ops.quantized.threshold(input, threshold, value)
