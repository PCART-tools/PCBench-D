@register_decomposition(aten.permute)
def permute(a: TensorLikeType, *dims) -> TensorLikeType:
    _permutation = utils.canonicalize_dims(
        a.ndim, utils.extract_dims_from_varargs(dims)
    )
    return prims.transpose(a, _permutation)
