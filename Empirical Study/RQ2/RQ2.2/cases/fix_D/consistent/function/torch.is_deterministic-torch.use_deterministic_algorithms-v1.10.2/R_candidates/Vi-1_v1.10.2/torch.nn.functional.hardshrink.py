def hardshrink(input: Tensor, lambd: float = 0.5) -> Tensor:
    r"""
    hardshrink(input, lambd=0.5) -> Tensor

    Applies the hard shrinkage function element-wise

    See :class:`~torch.nn.Hardshrink` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(hardshrink, (input,), input, lambd=lambd)
    return torch.hardshrink(input, lambd)
