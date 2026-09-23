@register_decomposition([aten.sym_constrain_range_for_size.default])
def sym_constrain_range_for_size(
    symbol: torch.SymInt,
    *,
    min: Optional[torch.types.Number] = None,
    max: Optional[torch.types.Number] = None,
) -> None:
    return
