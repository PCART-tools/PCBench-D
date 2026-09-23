@register_decomposition(aten.hinge_embedding_loss)
def hinge_embedding_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    margin: float = 1.0,
    reduction: str = "mean",
) -> TensorLikeType:
    # loss_without_reduction = input if y == 1
    #                        = max(0, margin - input) if y == -1
    _check_reduction_value(reduction)
    margin_clamp = torch.clamp_min(margin - input, 0)
    output_margin = torch.where(target != 1, margin_clamp, 0)
    output_self = torch.where(target != -1, input, 0)
    loss = output_margin + output_self
    return _apply_loss_reduction(loss, reduction)
