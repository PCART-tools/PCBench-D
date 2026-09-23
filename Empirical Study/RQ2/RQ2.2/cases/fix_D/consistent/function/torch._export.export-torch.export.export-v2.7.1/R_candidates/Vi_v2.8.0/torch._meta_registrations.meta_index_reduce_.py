@register_meta(aten.index_reduce_.default)
def meta_index_reduce_(
    self: Tensor,
    dim: int,
    index: Tensor,
    source: torch.Tensor,
    reduce: str,
    *,
    include_self: bool = True,
) -> Tensor:
    return self
