@register_decomposition(aten.huber_loss)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("input", "target"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def huber_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    reduction: Union[str, int] = "mean",
    delta: float = 1.0,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.huber_loss
    """
    if type(reduction) is int:
        reduction = _reduction_int_to_str(reduction)
    _check_reduction_value(reduction)  # type: ignore[arg-type]
    torch._check(
        delta > 0,
        lambda: "huber_loss does not support non-positive values for delta.",
    )
    z = (input - target).abs()
    loss = torch.where(z < delta, 0.5 * z * z, delta * (z - 0.5 * delta))
    return _apply_loss_reduction(loss, reduction)  # type: ignore[arg-type]
