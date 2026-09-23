@register_decomposition(aten.pairwise_distance)
@out_wrapper()
def pairwise_distance(
    x1: TensorLikeType,
    x2: TensorLikeType,
    p: NumberType = 2.0,
    eps: NumberType = 1e-6,
    keepdim=False,
) -> TensorLikeType:
    return torch.linalg.vector_norm(x1 - x2 + eps, ord=p, dim=-1, keepdim=keepdim)
