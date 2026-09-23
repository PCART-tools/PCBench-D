@register_decomposition(aten.diag.out)
@out_wrapper()
def diag(
    self: TensorLikeType,
    offset: int = 0,
) -> TensorLikeType:
    ndim = self.dim()
    torch._check(
        ndim in (1, 2), lambda: f"diag(): Supports 1D or 2D tensors. Got {ndim}D"
    )
    if ndim == 1:
        return torch.diag_embed(self, offset)
    else:
        return torch.diagonal_copy(self, offset)
