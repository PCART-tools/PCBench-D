@register_decomposition(aten.nll_loss_forward)
@out_wrapper("output", "total_weight")
def nll_loss_forward(
    self: Tensor,
    target: Tensor,
    weight: Optional[Tensor],
    reduction: int,
    ignore_index: int,
) -> tuple[Tensor, Tensor]:
    assert self.dim() > 0 and self.dim() <= 2, "input tensor should be 1D or 2D"
    assert target.dim() <= 1, (
        "0D or 1D target tensor expected, multi-target not supported"
    )

    no_batch_dim = self.dim() == 1 and target.dim() == 0
    assert no_batch_dim or (self.shape[0] == target.shape[0]), (
        f"size mismatch (got input: {self.shape}, target: {target.shape})"
    )

    n_classes = self.shape[-1]

    assert weight is None or (weight.dim() == 1 and weight.numel() == n_classes), (
        f"weight tensor should be defined either for all {n_classes} classes or no classes "
        f"but got weight tensor of shape: {weight.shape}"
    )

    return _nll_loss_forward(self, target, weight, reduction, ignore_index)
