@register_decomposition(aten.all)
@out_wrapper()
def all(
    a: TensorLikeType,
    dim: Optional[DimsType] = None,
    keepdim: bool = False,
) -> TensorLikeType:
    result = torch.logical_not(torch.any(torch.logical_not(a), dim, keepdim=keepdim))

    if a.dtype == torch.uint8:
        result = result.to(dtype=torch.uint8)

    return result
