@elementwise_type_promotion_wrapper(
    type_promoting_args=("input", "target"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def poisson_nll_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    log_input: bool = True,
    full: bool = False,
    size_average: Optional[bool] = None,
    eps: float = 1e-8,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.poisson_nll_loss
    """
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)
    _check_reduction_value(reduction)
    if log_input:
        loss = torch.exp(input) - target * input
    else:
        loss = input - target * torch.log(input + eps)

    if full:
        stirling_term = (
            target * torch.log(target) - target + 0.5 * torch.log(2 * torch.pi * target)
        )
        # avoid inplace add
        loss = loss + stirling_term.masked_fill(target <= 1, 0)
    return _apply_loss_reduction(loss, reduction)
