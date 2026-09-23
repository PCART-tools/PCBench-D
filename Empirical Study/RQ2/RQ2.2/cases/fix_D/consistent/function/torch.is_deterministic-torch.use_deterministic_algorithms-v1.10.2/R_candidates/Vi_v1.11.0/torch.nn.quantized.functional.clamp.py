def clamp(input: Tensor, min_: float, max_: float) -> Tensor:
    r"""float(input, min\_, max\_) -> Tensor

    Applies the clamp function element-wise.
    See :class:`~torch.nn.quantized.clamp` for more details.

    Args:
        input: quantized input
        min_: minimum value for clamping
        max_: maximum value for clamping
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.clamp' must be quantized!")
    return torch.clamp(input, min_, max_)
