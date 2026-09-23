def layer_norm(
    input: Tensor,
    normalized_shape: ShapeType,
    weight: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    eps: float = 1e-5,
) -> Tensor:
    """
    Reference implementation of :func:`torch.nn.functional.layer_norm`.
    """
    return torch.native_layer_norm(input, normalized_shape, weight, bias, eps)[0]
