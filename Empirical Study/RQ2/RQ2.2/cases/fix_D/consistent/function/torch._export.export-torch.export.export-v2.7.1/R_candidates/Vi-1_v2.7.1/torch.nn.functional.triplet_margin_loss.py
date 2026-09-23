def triplet_margin_loss(
    anchor: Tensor,
    positive: Tensor,
    negative: Tensor,
    margin: float = 1.0,
    p: float = 2,
    eps: float = 1e-6,
    swap: bool = False,
    size_average: Optional[bool] = None,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
) -> Tensor:
    r"""Compute the triplet loss between given input tensors and a margin greater than 0.

    See :class:`~torch.nn.TripletMarginLoss` for details.
    """
    if has_torch_function_variadic(anchor, positive, negative):
        return handle_torch_function(
            triplet_margin_loss,
            (anchor, positive, negative),
            anchor,
            positive,
            negative,
            margin=margin,
            p=p,
            eps=eps,
            swap=swap,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    if margin <= 0:
        raise ValueError(f"margin must be greater than 0, got {margin}")
    return torch.triplet_margin_loss(
        anchor, positive, negative, margin, p, eps, swap, reduction_enum
    )
