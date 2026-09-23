@elementwise_type_promotion_wrapper(
    type_promoting_args=("input", "target"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.COMPLEX_TO_FLOAT,
)
def smooth_l1_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    size_average: Optional[bool] = None,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
    beta: float = 1.0,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.smooth_l1_loss
    """
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)
    _check_reduction_value(reduction)

    if beta == 0.0:
        return torch.nn.functional.l1_loss(
            input, target, size_average=size_average, reduce=reduce, reduction=reduction
        )
    else:
        loss = torch.abs(input - target)
        loss = torch.where(loss < beta, 0.5 * loss**2 / beta, loss - 0.5 * beta)
        return _apply_loss_reduction(loss, reduction)
