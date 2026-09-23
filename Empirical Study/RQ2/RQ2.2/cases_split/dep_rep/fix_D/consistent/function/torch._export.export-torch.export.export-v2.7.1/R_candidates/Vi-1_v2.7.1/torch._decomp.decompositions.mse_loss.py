@register_decomposition(aten.mse_loss)
@out_wrapper()
@pw_cast_for_opmath
def mse_loss(
    self: Tensor, target: Tensor, reduction: int = Reduction.MEAN.value
) -> Tensor:
    loss = (self - target) ** 2
    return apply_loss_reduction(loss, reduction)
