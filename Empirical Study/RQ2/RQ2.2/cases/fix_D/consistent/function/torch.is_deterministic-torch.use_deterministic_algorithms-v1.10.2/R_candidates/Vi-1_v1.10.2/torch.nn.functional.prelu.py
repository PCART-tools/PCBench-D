def prelu(input: Tensor, weight: Tensor) -> Tensor:
    r"""prelu(input, weight) -> Tensor

    Applies element-wise the function
    :math:`\text{PReLU}(x) = \max(0,x) + \text{weight} * \min(0,x)` where weight is a
    learnable parameter.

    See :class:`~torch.nn.PReLU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(prelu, (input,), input, weight)
    return torch.prelu(input, weight)
