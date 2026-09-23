def hardsigmoid(input: Tensor, inplace: bool = False) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardsigmoid`.
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardsigmoid' must be quantized!")
    if inplace:
        return torch._C._nn.hardsigmoid_(input)  # type: ignore[attr-defined]
    return torch._C._nn.hardsigmoid(input)
