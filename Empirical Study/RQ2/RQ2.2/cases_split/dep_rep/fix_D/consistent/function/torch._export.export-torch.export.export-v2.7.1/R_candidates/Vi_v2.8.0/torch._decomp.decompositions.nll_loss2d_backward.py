@register_decomposition(aten.nll_loss2d_backward)
@out_wrapper("grad_input")
def nll_loss2d_backward(
    grad_output: Tensor,
    self: Tensor,
    target: Tensor,
    weight: Optional[Tensor],
    reduction: int,
    ignore_index: int,
    total_weight: Tensor,
) -> Tensor:
    assert self.dim() == 4, (
        f"only batches of spatial inputs supported (4D tensors), but got input of dimension: {self.dim()}"
    )

    assert target.dim() == 3, (
        f"only batches of spatial targets supported (3D tensors) but got targets of dimension: {target.dim()}"
    )

    assert (
        self.shape[0] == target.shape[0]
        and self.shape[2] == target.shape[1]
        and self.shape[3] == target.shape[2]
    ), f"size mismatch (got input: {self.shape}, target: {target.shape}"

    assert total_weight.numel() == 1, (
        "expected total_weight to be a single element tensor, "
        f"got: {total_weight.shape} ( {total_weight.numel()}, elements)"
    )

    return _nll_loss_backward(
        grad_output, self, target, weight, reduction, ignore_index, total_weight
    )
