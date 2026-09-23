def leaky_relu(
    input: Tensor,
    negative_slope: float = 0.01,
    inplace: bool = False,
) -> Tensor:  # noqa: D400,D402
    r"""
    leaky_relu(input, negative_slope=0.01, inplace=False) -> Tensor

    Applies element-wise,
    :math:`\text{LeakyReLU}(x) = \max(0, x) + \text{negative\_slope} * \min(0, x)`

    See :class:`~torch.nn.LeakyReLU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            leaky_relu, (input,), input, negative_slope=negative_slope, inplace=inplace
        )
    if inplace:
        result = torch._C._nn.leaky_relu_(input, negative_slope)
    else:
        result = torch._C._nn.leaky_relu(input, negative_slope)
    return result
