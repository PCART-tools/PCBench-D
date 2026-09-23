def hardswish(input: Tensor, scale: float, zero_point: int) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardswish`.

    Args:
        input: quantized input
        scale: quantization scale of the output tensor
        zero_point: quantization zero point of the output tensor
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardswish' must be quantized!")
    return torch._ops.ops.quantized.hardswish(input, scale, zero_point)
