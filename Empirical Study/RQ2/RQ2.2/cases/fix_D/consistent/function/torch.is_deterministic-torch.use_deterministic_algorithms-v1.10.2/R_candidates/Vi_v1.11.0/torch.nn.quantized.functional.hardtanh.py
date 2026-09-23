def hardtanh(input: Tensor, min_val: float = -1., max_val: float = 1., inplace: bool = False) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardtanh`.
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardtanh' must be quantized!")
    if inplace:
        return torch._C._nn.hardtanh_(input, min_val, max_val)
    return torch._C._nn.hardtanh(input, min_val, max_val)
