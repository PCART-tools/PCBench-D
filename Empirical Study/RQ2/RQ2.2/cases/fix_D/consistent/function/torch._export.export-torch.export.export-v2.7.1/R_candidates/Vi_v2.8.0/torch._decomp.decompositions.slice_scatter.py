@register_decomposition(aten.slice_scatter)
@out_wrapper()
def slice_scatter(
    input: Tensor,
    src: Tensor,
    dim: int = 0,
    start: Optional[int] = None,
    end: Optional[int] = None,
    step: int = 1,
):
    dim = utils.canonicalize_dim(input.ndim, dim)
    dim_size = input.shape[dim]
    start, end = _normalize_start_end(input, dim, start, end)

    src_size = list(input.shape)
    src_size[dim] = (end - start + (step - 1)) // step
    src = src.expand(src_size)

    if start == 0 and end == dim_size and step == 1:
        return src.clone()

    indices = [None] * input.dim()
    idx = torch.arange(dim_size, device=input.device)
    indices[dim] = (idx - start) // step

    mask = torch.ones(dim_size, device=input.device, dtype=torch.bool)
    if start != 0:
        mask = torch.logical_and(mask, idx >= start)

    if end != dim_size:
        mask = torch.logical_and(mask, idx < end)

    if step != 1:
        mask = torch.logical_and(mask, (idx - start) % step == 0)

    mask_shape = [1] * input.dim()
    mask_shape[dim] = -1
    mask = mask.view(mask_shape)
    return aten.where(mask, aten._unsafe_masked_index(src, mask, indices, 0), input)
