@register_decomposition(torch._ops.ops.aten.linalg_cross)
@out_wrapper()
@pw_cast_for_opmath
def cross(a: Tensor, b: Tensor, dim: int = -1):
    torch._check(
        a.ndim == b.ndim,
        lambda: "linalg.cross: inputs must have the same number of dimensions.",
    )
    torch._check(
        a.size(dim) == 3 and b.size(dim) == 3,
        lambda: f"linalg.cross: inputs dim {dim} must have length 3, got {a.size(dim)} and {b.size(dim)}",
    )
    a, b = torch.broadcast_tensors(a, b)
    dim = utils.canonicalize_dim(a.ndim, dim)
    idx = torch.arange(3, device=a.device)
    return a.index_select(dim, (idx + 1) % 3) * b.index_select(
        dim, (idx + 2) % 3
    ) - a.index_select(dim, (idx + 2) % 3) * b.index_select(dim, (idx + 1) % 3)
