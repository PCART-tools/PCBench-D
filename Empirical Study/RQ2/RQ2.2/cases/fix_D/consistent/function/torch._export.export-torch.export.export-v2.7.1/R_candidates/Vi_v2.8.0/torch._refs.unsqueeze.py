@register_decomposition(aten.unsqueeze)
def unsqueeze(a: TensorLikeType, dim: int) -> TensorLikeType:
    # Note that unsqueeze canonicalizes with rank + 1 because it allows
    # a new innermost dimension to be specified
    ndim = a.ndim + 1
    dim = utils.canonicalize_dim(ndim, dim)
    return prims.expand_dims(a, (dim,), ndim=ndim)
