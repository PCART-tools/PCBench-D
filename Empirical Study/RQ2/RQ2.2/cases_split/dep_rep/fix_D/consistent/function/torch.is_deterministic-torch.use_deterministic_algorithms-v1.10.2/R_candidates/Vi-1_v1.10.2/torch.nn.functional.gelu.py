def gelu(input):
    r"""gelu(input) -> Tensor

    Applies element-wise the function
    :math:`\text{GELU}(x) = x * \Phi(x)`

    where :math:`\Phi(x)` is the Cumulative Distribution Function for Gaussian Distribution.

    See `Gaussian Error Linear Units (GELUs) <https://arxiv.org/abs/1606.08415>`_.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(gelu, (input,), input)
    return torch._C._nn.gelu(input)
