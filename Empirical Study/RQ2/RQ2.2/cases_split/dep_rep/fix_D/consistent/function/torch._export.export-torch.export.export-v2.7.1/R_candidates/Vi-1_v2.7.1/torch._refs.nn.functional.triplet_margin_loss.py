def triplet_margin_loss(
    anchor: TensorLikeType,
    positive: TensorLikeType,
    negative: TensorLikeType,
    margin: float = 1.0,
    p: float = 2,
    eps: float = 1e-6,
    swap: bool = False,
    size_average: Optional[bool] = None,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
) -> TensorLikeType:
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)

    if margin <= 0:
        raise ValueError(f"margin must be greater than 0, got {margin}")

    # torch.nn.functional.triplet_margin_with_distance_loss has no ref defined
    # since it's a pure Python implementation.  Use this helper instead.
    return _triplet_margin_with_distance_loss(
        anchor=anchor,
        positive=positive,
        negative=negative,
        distance_function=lambda x, y: torch.pairwise_distance(x, y, p, eps),
        margin=margin,
        swap=swap,
        reduction=reduction,
    )
