@register_decomposition(aten.index_select)
@out_wrapper()
def index_select(x: TensorLike, dim: int, index: TensorLike):
    dim = utils.canonicalize_dims(x.ndim, dim)
    torch._check(
        index.ndim <= 1,
        lambda: f"Index should have dimension 1 or 0 (got {index.ndim})",
    )
    if index.ndim == 0:
        index = index.unsqueeze(0)
    if x.ndim == 0:
        # Treat scalars as elements of \R^1
        # We cannot use x[idx] here as it accesses item() (??), hence this awkward construction
        return torch.empty_like(x).index_copy(0, index, x.expand_as(index))

    idx = (slice(None),) * dim + (index,)
    return x[idx]
