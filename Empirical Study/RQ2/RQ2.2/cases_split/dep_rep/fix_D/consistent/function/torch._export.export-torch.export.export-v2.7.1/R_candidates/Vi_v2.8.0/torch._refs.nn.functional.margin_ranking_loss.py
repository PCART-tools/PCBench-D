@register_decomposition(aten.margin_ranking_loss)
def margin_ranking_loss(
    input1: TensorLikeType,
    input2: TensorLikeType,
    target: TensorLikeType,
    margin: float = 0.0,
    reduction: str = "mean",
) -> TensorLikeType:
    # loss_without_reduction = max(0, -target * (input1 - input2) + margin)
    if input1.ndim != input2.ndim or input1.ndim != target.ndim:
        raise RuntimeError(
            "margin_ranking_loss : All input tensors should have same dimension but got sizes: "
            f"input1: {input1.shape}, input2: {input2.shape}, target: {target.shape} "
        )
    _check_reduction_value(reduction)
    loss = torch.clamp_min(-target * (input1 - input2) + margin, 0)
    return _apply_loss_reduction(loss, reduction)
