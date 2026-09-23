def selu(input: Tensor, inplace: bool = False) -> Tensor:
    r"""selu(input, inplace=False) -> Tensor

    Applies element-wise,
    :math:`\text{SELU}(x) = scale * (\max(0,x) + \min(0, \alpha * (\exp(x) - 1)))`,
    with :math:`\alpha=1.6732632423543772848170429916717` and
    :math:`scale=1.0507009873554804934193349852946`.

    See :class:`~torch.nn.SELU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(selu, (input,), input, inplace=inplace)
    if inplace:
        result = torch.selu_(input)
    else:
        result = torch.selu(input)
    return result
