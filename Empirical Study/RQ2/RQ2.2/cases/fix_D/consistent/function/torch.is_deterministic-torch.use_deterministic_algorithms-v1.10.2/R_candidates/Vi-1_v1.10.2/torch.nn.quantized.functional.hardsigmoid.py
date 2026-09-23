def hardsigmoid(input: Tensor) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardsigmoid`.
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardsigmoid' must be quantized!")
    return torch._C._nn.hardsigmoid(input)
