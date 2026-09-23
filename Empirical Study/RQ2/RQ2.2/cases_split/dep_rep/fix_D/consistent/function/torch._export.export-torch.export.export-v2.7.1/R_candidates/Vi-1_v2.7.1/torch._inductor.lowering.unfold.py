@register_lowering(aten.unfold, type_promotion_kind=None)
def unfold(x, dimension, size, step):
    sizes = x.get_size()
    ndim = len(sizes)
    dim = canonicalize_dim(ndim, dimension)

    if ndim == 0:
        return slice_(unsqueeze(x, 0), end=size)

    dim_size = sizes[dim]
    sizevars = V.graph.sizevars
    sizevars.guard_leq(size, dim_size)
    sizevars.guard_lt(0, step)  # type: ignore[arg-type]

    new_dim_size = FloorDiv(dim_size - size, step) + 1
    if sizevars.size_hint(dim_size) > 0:
        x.mark_reuse(sizevars.size_hint(CeilDiv(new_dim_size * size, dim_size)))

    out_size = [*sizes[:dim], new_dim_size, *sizes[dim + 1 :], size]

    def reindexer(idx):
        dim_idx = idx[-1] + idx[dim] * step
        return (*idx[:dim], dim_idx, *idx[dim + 1 : -1])

    return TensorBox(ir.GenericView.create(x, out_size, reindexer))
