@register_decomposition(aten.nll_loss2d_forward)
@out_wrapper("output", "total_weight")
def nll_loss2d_forward(
    self: Tensor,
    target: Tensor,
    weight: Optional[Tensor],
    reduction: int,
    ignore_index: int,
) -> tuple[Tensor, Tensor]:
    return _nll_loss_forward(self, target, weight, reduction, ignore_index)
