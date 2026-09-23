def uniform_(tensor: Tensor, a: float = 0., b: float = 1.) -> Tensor:
    r"""Fills the input Tensor with values drawn from the uniform
    distribution :math:`\mathcal{U}(a, b)`.

    Args:
        tensor: an n-dimensional `torch.Tensor`
        a: the lower bound of the uniform distribution
        b: the upper bound of the uniform distribution

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.uniform_(w)
    """
    if torch.overrides.has_torch_function_variadic(tensor):
        return torch.overrides.handle_torch_function(uniform_, (tensor,), tensor=tensor, a=a, b=b)
    return _no_grad_uniform_(tensor, a, b)
