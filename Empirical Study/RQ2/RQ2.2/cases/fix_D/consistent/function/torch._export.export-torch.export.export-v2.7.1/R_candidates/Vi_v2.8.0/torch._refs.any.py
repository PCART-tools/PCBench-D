@register_decomposition(aten.any)
@out_wrapper()
def any(
    a: TensorLikeType,
    dim: Optional[DimsType] = None,
    keepdim: bool = False,
) -> TensorLikeType:
    a_ = _maybe_convert_to_dtype(a, torch.bool)
    if isinstance(dim, (list, tuple)) and len(dim) == 0:
        result = a_.clone()
    else:
        result = a_.sum(dim=dim, keepdim=keepdim).ne(False)

    # Preserves uint8 -- probably a legacy mask thing
    if a.dtype is torch.uint8:
        return prims.convert_element_type(result, torch.uint8)

    return result
