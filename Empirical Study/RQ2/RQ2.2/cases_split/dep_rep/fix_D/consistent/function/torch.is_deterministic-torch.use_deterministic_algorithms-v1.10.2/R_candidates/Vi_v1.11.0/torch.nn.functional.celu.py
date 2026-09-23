def celu(input: Tensor, alpha: float = 1.0, inplace: bool = False) -> Tensor:
    r"""celu(input, alpha=1., inplace=False) -> Tensor

    Applies element-wise,
    :math:`\text{CELU}(x) = \max(0,x) + \min(0, \alpha * (\exp(x/\alpha) - 1))`.

    See :class:`~torch.nn.CELU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(celu, (input,), input, alpha=alpha, inplace=inplace)
    if inplace:
        result = torch.celu_(input, alpha)
    else:
        result = torch.celu(input, alpha)
    return result
