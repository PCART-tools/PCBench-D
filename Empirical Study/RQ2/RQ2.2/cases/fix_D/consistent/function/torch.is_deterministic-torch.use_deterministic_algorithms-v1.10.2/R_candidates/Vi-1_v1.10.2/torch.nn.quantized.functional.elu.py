def elu(input: Tensor, scale: float, zero_point: int, alpha: float = 1.) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.elu`.

    Args:
        input: quantized input
        scale: quantization scale of the output tensor
        zero_point: quantization zero point of the output tensor
        alpha: the alpha constant
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.elu' must be quantized!")
    return torch.ops.quantized.elu(input, scale, zero_point, alpha)
