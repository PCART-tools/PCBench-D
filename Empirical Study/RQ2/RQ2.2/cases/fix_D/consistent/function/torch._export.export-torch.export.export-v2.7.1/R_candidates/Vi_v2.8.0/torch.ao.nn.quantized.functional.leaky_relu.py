def leaky_relu(
    input: Tensor,
    negative_slope: float = 0.01,
    inplace: bool = False,
    scale: Optional[float] = None,
    zero_point: Optional[int] = None,
):
    r"""
    Quantized version of the.
    leaky_relu(input, negative_slope=0.01, inplace=False, scale, zero_point) -> Tensor

    Applies element-wise,
    :math:`\text{LeakyReLU}(x) = \max(0, x) + \text{negative\_slope} * \min(0, x)`

    Args:
        input: Quantized input
        negative_slope: The slope of the negative input
        inplace: Inplace modification of the input tensor
        scale, zero_point: Scale and zero point of the output tensor.

    See :class:`~torch.nn.LeakyReLU` for more details.
    """
    if scale is not None and zero_point is not None:
        assert not inplace, "Cannot rescale with `inplace`"
        output = torch._empty_affine_quantized(
            input.shape, scale=scale, zero_point=int(zero_point), dtype=input.dtype
        )
        torch._C._nn.leaky_relu(input, negative_slope, out=output)
        return output
    if inplace:
        result = torch._C._nn.leaky_relu_(input, negative_slope)
    else:
        result = torch._C._nn.leaky_relu(input, negative_slope)
    return result
