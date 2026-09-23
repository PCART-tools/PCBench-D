@register_lowering(aten.sort.stable, type_promotion_kind=None)
def sort_stable(x, *, stable=None, dim=-1, descending=False):
    if stable is None:
        stable = False

    shape = x.get_size()
    device = x.get_device()
    dim = canonicalize_dim(len(shape), dim)
    if len(shape) == 0:
        return clone(x), _full(0, device, torch.int64, shape)

    dim_size = shape[dim] if len(shape) else 1
    if not V.graph.sizevars.statically_known_lt(dim_size, torch.iinfo(torch.int16).max):
        return sort_fallback(x, stable=stable, dim=dim, descending=descending)

    indices = iota(
        dim_size, start=0, step=1, dtype=torch.int16, device=device, requires_grad=False
    )
    view_shape = [1] * len(shape)
    if len(shape):
        view_shape[dim] = dim_size
    indices = view(indices, view_shape)
    indices = expand(indices, shape)

    values, indices = ir.Sort.create(
        device=device,
        dtypes=(x.dtype, indices.dtype),
        inner_fns=(x.make_loader(), indices.make_loader()),
        size=shape,
        axis=dim,
        stable=stable,
        descending=descending,
    )
    if values is None:
        return sort_fallback(x, stable=stable, dim=dim, descending=descending)

    assert indices is not None
    return values, to_dtype(indices, torch.int64)
