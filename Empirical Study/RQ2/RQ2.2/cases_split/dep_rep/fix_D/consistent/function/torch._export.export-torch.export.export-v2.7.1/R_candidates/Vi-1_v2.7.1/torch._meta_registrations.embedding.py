@register_meta(aten.embedding)
@out_wrapper()
def embedding(
    weight: Tensor,
    indices: Tensor,
    padding_idx: int = -1,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
) -> Tensor:
    assert weight.dim() == 2, "'weight' must be 2-D"
    weight_shape = weight.shape
    indices_shape = indices.shape

    if indices.ndim == 0:
        out_shape: tuple[int, ...] = (weight_shape[1],)
    elif indices.ndim == 1:
        out_shape = (indices_shape[0], weight_shape[1])
    else:
        out_shape = (*indices_shape, weight_shape[1])

    out_dtype = weight.dtype
    return weight.new_empty(out_shape, dtype=out_dtype)
