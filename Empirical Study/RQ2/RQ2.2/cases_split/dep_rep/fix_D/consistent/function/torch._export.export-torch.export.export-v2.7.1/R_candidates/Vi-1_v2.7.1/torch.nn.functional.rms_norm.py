def rms_norm(
    input: Tensor,
    normalized_shape: list[int],
    weight: Optional[Tensor] = None,
    eps: Optional[float] = None,
) -> Tensor:
    r"""Apply Root Mean Square Layer Normalization.

    See :class:`~torch.nn.RMSNorm` for details.
    """
    if has_torch_function_variadic(input, weight):
        return handle_torch_function(
            rms_norm, (input, weight), input, normalized_shape, weight=weight, eps=eps
        )
    return torch.rms_norm(input, normalized_shape, weight, eps)
