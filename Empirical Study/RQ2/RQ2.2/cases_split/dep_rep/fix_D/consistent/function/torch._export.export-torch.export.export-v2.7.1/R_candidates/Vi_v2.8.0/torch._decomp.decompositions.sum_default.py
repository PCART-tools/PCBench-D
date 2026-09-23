@register_decomposition([aten.sum.default, aten.sum.out])
def sum_default(
    self: Tensor,
    *,
    dtype: Optional[torch.dtype] = None,
    out: Optional[Tensor] = None,
) -> Tensor:
    if out is None:
        return aten.sum.dim_IntList(self, [], dtype=dtype)
    else:
        return aten.sum.IntList_out(self, [], dtype=dtype, out=out)
