@register_decomposition(aten.searchsorted.Scalar)
def searchsorted_scalar(
    sorted_sequence: torch.Tensor,
    self: torch.types.Number,
    *,
    out_int32: bool = False,
    right: bool = False,
    side: Optional[str] = None,
    sorter: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return aten.searchsorted(
        sorted_sequence,
        torch.tensor([self], device=sorted_sequence.device),
        out_int32=out_int32,
        right=right,
        side=side,
        sorter=sorter,
    )[0]
