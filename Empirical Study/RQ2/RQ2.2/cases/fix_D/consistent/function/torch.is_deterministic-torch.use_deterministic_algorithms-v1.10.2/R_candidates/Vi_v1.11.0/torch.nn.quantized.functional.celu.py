def celu(input: Tensor, scale: float, zero_point: int, alpha: float = 1.) -> Tensor:
    r"""celu(input, scale, zero_point, alpha=1.) -> Tensor

    Applies the quantized CELU function element-wise.

    .. math::
        \text{CELU}(x) = \max(0,x) + \min(0, \alpha * (\exp(x / \alpha) - 1))

    Args:
        input: quantized input
        alpha: the :math:`\alpha` value for the CELU formulation. Default: 1.0
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.celu' must be quantized!")
    return torch.ops.quantized.celu(input, scale, zero_point, alpha)
