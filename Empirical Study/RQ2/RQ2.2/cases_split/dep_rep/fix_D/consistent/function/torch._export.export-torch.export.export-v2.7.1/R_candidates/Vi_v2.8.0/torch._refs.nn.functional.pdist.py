@register_decomposition(aten.pdist)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def pdist(a: TensorLikeType, p: float = 2) -> TensorLikeType:
    torch._check(a.ndim == 2, lambda: f"pdist only supports 2D tensors, got: {a.ndim}D")
    torch._check(p >= 0, lambda: "pdist only supports non-negative p values")
    # For p == 2 we can use an efficient implementation, but other values of p
    # require creating a much bigger tensor for an intermediate step
    if p == 2:
        aTa = torch.mm(a, a.T)
        aTa_diag = torch.diag(aTa)
        t = torch.sqrt(torch.clamp(aTa_diag + aTa_diag.unsqueeze(-1) - 2 * aTa, min=0))
    else:
        t = torch.linalg.vector_norm(a.unsqueeze(1) - a, ord=p, dim=2)
    i = torch.triu_indices(t.shape[0], t.shape[1], offset=1, device=a.device)
    return t.flatten().index_select(0, i[0] * t.shape[0] + i[1])
